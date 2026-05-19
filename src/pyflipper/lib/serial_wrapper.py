

import socket
import serial
import re
from websocket import create_connection

def error_handler(func):
    def handler(*args):
        result = func(*args)
        pattern = re.compile(r"\w+\serror:\s.*")
        match = pattern.match(result)
        if match:
            raise Exception(match.group())
        return result        
    return handler

class LocalSerial:
    def __init__(self, com) -> None:
        self._serial_port = serial.Serial(port=com, baudrate=9600,
                                         bytesize=8, timeout=None, stopbits=serial.STOPBITS_ONE)
        self._serial_port.write(f"\n\n\r".encode())
        self._serial_port.read_until(b'>:') #skip welcome banner

    @error_handler
    def send(self, payload: str) -> str:
        # empty buffer before sending
        try:
            self._serial_port.reset_input_buffer()
        except AttributeError:
            # fallback: in case reset_input_buffer is not available, read until empty
            while self._serial_port.in_waiting:
                self._serial_port.read(self._serial_port.in_waiting)

        self._serial_port.write(f"{payload}\r".encode())

        # await echo
        try:
            self._serial_port.read_until(f"{payload}\r".encode())
        except Exception:
            # continue if timing out
            pass

        # read until prompted again and decode
        raw_response = self._serial_port.read_until(b'>:').decode(errors='ignore')

        # removing echo and prompt
        raw_response = raw_response.split(f"{payload}\r\n", 1)[-1] if f"{payload}\r\n" in raw_response else raw_response.replace(f"{payload}\r", "", 1)
        raw_response = raw_response.replace('>:', '').strip()

        return raw_response


    def write(self, msg):
        self._serial_port.write(msg)
    
    def ctrl_c(self):
        self._serial_port.write(b'\x03')

class WSSerial:
    def __init__(self, ws) -> None:
        self.ws = create_connection(ws)
        self.ws.recv() #skip welcome

    @error_handler
    def send(self, payload: str) -> str:
        self.ws.send_binary(f"{payload}\r".encode())
        line = ""
        while ">:" not in line:
            line += self.ws.recv()
        return line.split(f'{payload}\r\n')[-1].rstrip('\r\n>: ')
    
    def write(self, msg):
        self.ws.send_binary(msg)

    def ctrl_c(self):
        self.ws.send_binary(b'\x03')

class TcpSerial:
    def __init__(self, addr) -> None:
        host, _, port = addr.partition(':')
        port = int(port)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._read_response()

    @error_handler
    def send(self, payload: str) -> str:
        self._socket.sendall(f"{payload}\r".encode())
        return self._read_response()

    def write(self, msg):
        self._socket.sendall(msg)

    def ctrl_c(self):
        self._socket.sendall(b'\x03')

    def _read_response(self):
        buff = ''
        while True:
            buff += self._socket.recv(1024).decode()
            if '>:' in buff:
                break
        return '\n'.join(buff.splitlines()[1:-2])
