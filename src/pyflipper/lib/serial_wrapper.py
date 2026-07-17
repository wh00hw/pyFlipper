import socket
import re
import time

import serial
from websocket import create_connection

# The Flipper CLI prints this prompt after every command's output. The real
# prompt is ``>: `` (trailing space); we read up to ``>:`` so both the spaced
# and unspaced variants are handled.
PROMPT = b">:"

_ERROR_PATTERN = re.compile(r"\w+\serror:\s.*")
# Current firmware echoes typed input through an ANSI line editor, so replies
# may contain cursor/erase escape sequences we need to drop before parsing.
_ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?=]*[A-Za-z]")


def _clean_response(raw: str, payload: str) -> str:
    """Strip the echoed command and the trailing prompt from a CLI reply.

    A raw Flipper reply for ``<cmd>`` looks like ``<cmd>\\r\\n<output>\\r\\n>:``.
    We drop the leading command echo and the trailing prompt, returning just
    ``<output>``.
    """
    raw = _ANSI_PATTERN.sub("", raw)
    # Remove the command echo. The firmware echoes the command followed by a
    # CRLF; some transports strip the CR, so tolerate both.
    for marker in (f"{payload}\r\n", f"{payload}\n"):
        if marker in raw:
            raw = raw.split(marker, 1)[1]
            break
    else:
        if raw.startswith(payload):
            raw = raw[len(payload):]

    # Remove the trailing prompt (and any whitespace around it).
    raw = raw.rstrip()
    if raw.endswith(">:"):
        raw = raw[:-2]

    return raw.strip("\r\n")


def error_handler(func):
    def handler(*args, **kwargs):
        result = func(*args, **kwargs)
        match = _ERROR_PATTERN.match(result or "")
        if match:
            raise Exception(match.group())
        return result
    return handler


class LocalSerial:
    def __init__(self, com) -> None:
        self._serial_port = serial.Serial(
            port=com, baudrate=9600, bytesize=8, timeout=1,
            stopbits=serial.STOPBITS_ONE,
        )
        self._serial_port.write(b"\r")
        self._serial_port.read_until(PROMPT)  # skip welcome banner

    @error_handler
    def send(self, payload: str) -> str:
        # Drop anything left in the buffer from a previous interaction so the
        # echo/prompt bookkeeping stays aligned.
        try:
            self._serial_port.reset_input_buffer()
        except (AttributeError, OSError):
            pass
        self._serial_port.write(f"{payload}\r".encode())
        raw = self._serial_port.read_until(PROMPT).decode(errors="ignore")
        return _clean_response(raw, payload)

    def write(self, msg) -> None:
        self._serial_port.write(msg)

    def read_until_prompt(self) -> str:
        return self._serial_port.read_until(PROMPT).decode(errors="ignore")

    def capture(self, seconds: float, marker: bytes = None) -> str:
        # Read whatever the device emits for up to `seconds`, returning early if
        # `marker` is seen. Used for interactive commands (sub-shells, scanners).
        deadline = time.monotonic() + seconds
        buf = bytearray()
        while time.monotonic() < deadline:
            waiting = getattr(self._serial_port, "in_waiting", 0)
            if waiting:
                buf += self._serial_port.read(waiting)
                if marker and marker in buf:
                    break
            else:
                time.sleep(0.02)
        return _ANSI_PATTERN.sub("", buf.decode(errors="ignore"))

    def ctrl_c(self) -> None:
        self._serial_port.write(b"\x03")

    def close(self) -> None:
        self._serial_port.close()


class WSSerial:
    def __init__(self, ws) -> None:
        self.ws = create_connection(ws)
        self._recv_until_prompt()  # skip welcome banner

    def _recv_until_prompt(self) -> str:
        line = ""
        while ">:" not in line:
            line += self.ws.recv()
        return line

    @error_handler
    def send(self, payload: str) -> str:
        self.ws.send_binary(f"{payload}\r".encode())
        return _clean_response(self._recv_until_prompt(), payload)

    def write(self, msg) -> None:
        self.ws.send_binary(msg)

    def read_until_prompt(self) -> str:
        return self._recv_until_prompt()

    def capture(self, seconds: float, marker: bytes = None) -> str:
        marker_txt = marker.decode() if marker else None
        self.ws.settimeout(0.2)
        deadline = time.monotonic() + seconds
        buf = ""
        while time.monotonic() < deadline:
            try:
                chunk = self.ws.recv()
            except Exception:
                continue
            buf += chunk.decode(errors="ignore") if isinstance(chunk, bytes) else chunk
            if marker_txt and marker_txt in buf:
                break
        return _ANSI_PATTERN.sub("", buf)

    def ctrl_c(self) -> None:
        self.ws.send_binary(b"\x03")

    def close(self) -> None:
        self.ws.close()


class TcpSerial:
    def __init__(self, addr) -> None:
        host, _, port = addr.partition(":")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, int(port)))
        self._recv_until_prompt()  # skip welcome banner

    def _recv_until_prompt(self) -> str:
        buff = ""
        while ">:" not in buff:
            chunk = self._socket.recv(1024)
            if not chunk:
                break
            buff += chunk.decode(errors="ignore")
        return buff

    @error_handler
    def send(self, payload: str) -> str:
        self._socket.sendall(f"{payload}\r".encode())
        return _clean_response(self._recv_until_prompt(), payload)

    def write(self, msg) -> None:
        self._socket.sendall(msg)

    def read_until_prompt(self) -> str:
        return self._recv_until_prompt()

    def capture(self, seconds: float, marker: bytes = None) -> str:
        marker_txt = marker.decode() if marker else None
        self._socket.settimeout(0.2)
        deadline = time.monotonic() + seconds
        buf = ""
        while time.monotonic() < deadline:
            try:
                chunk = self._socket.recv(1024)
            except socket.timeout:
                continue
            if not chunk:
                break
            buf += chunk.decode(errors="ignore")
            if marker_txt and marker_txt in buf:
                break
        return _ANSI_PATTERN.sub("", buf)

    def ctrl_c(self) -> None:
        self._socket.sendall(b"\x03")

    def close(self) -> None:
        self._socket.close()
