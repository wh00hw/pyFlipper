class Gpio:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def mode(self, pin_name, value):
        #Set gpio mode: 0 - input, 1 - output
        return self._serial_wrapper.send(f"gpio mode {pin_name} {value}")
    
    def set(self, pin_name, value):
        return self._serial_wrapper.send(f"gpio set {pin_name} {value}")
    
    def read(self, pin_name):
        return self._serial_wrapper.send(f"gpio read {pin_name}")