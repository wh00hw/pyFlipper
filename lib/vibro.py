from .serial_wrapper import SerialWrapper

class Vibro:
    def __init__(self, serial_wrapper: SerialWrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def set(self, value: bool):
        assert isinstance(value, bool), \
            "Value must be boolean (True or False)."
        self._serial_wrapper.send(f"vibro {1 if value else 0}")
    
    def on(self):
        self._serial_wrapper.send(f"vibro 1")

    def off(self):
        self._serial_wrapper.send(f"vibro 0")