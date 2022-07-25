from .serial_wrapper import SerialWrapper

class Led:
    def __init__(self, serial_wrapper: SerialWrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def set(self, led: str, value: int):
        assert 0 <= value <= 255, "Value must be in 0-255 range."
        assert led in ("r", "b", "g", "bl"), \
            "Color must be 'r', 'b', 'g' or 'bl' for backlight."

        self._serial_wrapper.send(f"led {led} {value}")