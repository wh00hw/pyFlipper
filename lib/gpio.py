
class Gpio:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def mode(self, pin_name: str, value: int) -> str:
        #Set gpio mode: 0 - input, 1 - output
        return self._serial_wrapper.send(f"gpio mode {pin_name} {value}")
    
    def set(self, pin_name: str, value: int) -> str:
        return self._serial_wrapper.send(f"gpio set {pin_name} {value}")
    
    def read(self, pin_name: str) -> str:
        return self._serial_wrapper.send(f"gpio read {pin_name}")