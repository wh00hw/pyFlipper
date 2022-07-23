import time
import serial

class SerialWrapper:
    def __init__(self, port) -> None:
        self.serial_port = serial.Serial(port=port, baudrate=9600,
                                         bytesize=8, timeout=None, stopbits=serial.STOPBITS_ONE)
        self.serial_port.read_until(b'>')

    def send(self, payload):
        self.serial_port.read()
        self.serial_port.write(f"{payload}\r".encode())
        time.sleep(0.5)
        self.serial_port.readline()
        return self.serial_port.read_until(b'>').decode().rstrip('>\r\n')
    
    def ctrl_c(self):
        self.serial_port.write(b'\x03')
