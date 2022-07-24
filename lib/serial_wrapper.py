import time
import serial
import re

def error_handler(func):
    def handler(*args):
        result = func(*args)
        pattern = re.compile("\w+\serror:\s.*")
        match = pattern.match(result)
        if match:
            raise Exception(match.group())
        return result        
    return handler

class SerialWrapper:
    def __init__(self, port) -> None:
        self._serial_port = serial.Serial(port=port, baudrate=9600,
                                         bytesize=8, timeout=None, stopbits=serial.STOPBITS_ONE)
        self._serial_port.read_until(b'>:')

    @error_handler
    def send(self, payload: str) -> str:
        self._serial_port.write(f"{payload}\r".encode())
        time.sleep(0.5)
        self._serial_port.readline()
        return self._serial_port.read_until(b'>:').decode().rstrip('\r\n')
    
    def ctrl_c(self):
        self._serial_port.write(b'\x03')
