"""Hardware-free fakes that emulate the Flipper Zero CLI framing.

The real Flipper CLI, when you send ``<cmd>\\r`` over the virtual serial port,
echoes the command back, prints the command output, and finishes with the
prompt ``\\r\\n>: ``.  So a single request/response looks like::

    <cmd>\\r\\n<output>\\r\\n>:

These fakes reproduce that framing so the whole library can be exercised
without a physical device.  A test registers canned responses keyed by the
command string and the fake returns the correctly-framed bytes.
"""

PROMPT = b">: "


class FakeSerialPort:
    """A stand-in for ``serial.Serial`` used by ``LocalSerial``.

    It understands only the handful of methods the wrapper calls: ``write``,
    ``read_until``, ``readline``, ``reset_input_buffer``, ``read`` and the
    ``in_waiting`` property.
    """

    def __init__(self, responses=None, banner="Welcome to Flipper Zero",
                 subshells=None):
        # responses: mapping of command (without trailing CR) -> output text
        self.responses = dict(responses or {})
        # subshells: {enter_cmd: {subcmd: output}} — e.g. {"nfc": {"scanner": ...}}
        self.subshells = {k: dict(v) for k, v in (subshells or {}).items()}
        self._subshell = None
        self.timeout = None
        self.written = []
        # Start with the welcome banner + prompt already in the buffer, exactly
        # like a freshly opened connection.
        self._buffer = bytearray(f"{banner}\r\n".encode() + PROMPT)

    # -- helpers ---------------------------------------------------------
    def set_response(self, command, output):
        self.responses[command] = output

    def _subprompt(self):
        return f"[{self._subshell}]>: ".encode()

    def _queue_response(self, command):
        if self._subshell is not None:
            if command == "exit":
                self._subshell = None
                self._buffer.extend(f"{command}\r\n".encode() + PROMPT)
                return
            output = self.subshells[self._subshell].get(command, "")
            self._buffer.extend(f"{command}\r\n{output}\r\n".encode() + self._subprompt())
            return
        if command in self.subshells:
            self._subshell = command
            self._buffer.extend(f"{command}\r\n".encode() + self._subprompt())
            return
        output = self.responses.get(command, "")
        frame = f"{command}\r\n{output}\r\n".encode() + PROMPT
        self._buffer.extend(frame)

    # -- serial.Serial API ----------------------------------------------
    @property
    def in_waiting(self):
        return len(self._buffer)

    def reset_input_buffer(self):
        self._buffer = bytearray()

    def write(self, data):
        self.written.append(bytes(data))
        text = bytes(data).decode(errors="ignore")
        # Ctrl-C breaks out of a running listener; inside a sub-shell it returns
        # to the sub-prompt.
        if text == "\x03":
            if self._subshell is not None:
                self._buffer.extend(self._subprompt())
            return len(data)
        # A command is anything terminated by a carriage return.
        if text.endswith("\r") and text != "\r":
            self._queue_response(text[:-1])
        return len(data)

    def read(self, size=1):
        chunk = bytes(self._buffer[:size])
        del self._buffer[:size]
        return chunk

    def read_until(self, expected=b"\n", size=None):
        idx = self._buffer.find(expected)
        if idx == -1:
            out = bytes(self._buffer)
            self._buffer = bytearray()
            return out
        end = idx + len(expected)
        out = bytes(self._buffer[:end])
        del self._buffer[:end]
        return out

    def readline(self):
        return self.read_until(b"\n")

    def close(self):
        self._buffer = bytearray()
