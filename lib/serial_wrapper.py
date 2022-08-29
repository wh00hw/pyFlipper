
import time
import serial
import re
from websocket import create_connection

def error_handler(func):
    def handler(*args):
        result = func(*args)
        pattern = re.compile("\w+\serror:\s.*")
        match = pattern.match(result)
        if match:
            raise Exception(match.group())
        return result        
    return handler

class LocalSerial:
    def __init__(self, com) -> None:
        self._serial_port = serial.Serial(port=com, baudrate=9600,
                                         bytesize=8, timeout=None, stopbits=serial.STOPBITS_ONE)
        self._serial_port.read_until(b'>:') #skip welcome banner

    @error_handler
    def send(self, payload: str) -> str:
        self._serial_port.write(f"{payload}\r".encode())
        #time.sleep(0.5)
        self._serial_port.readline()
        return self._serial_port.read_until(b'>:').decode().rstrip('\r\n')
    
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