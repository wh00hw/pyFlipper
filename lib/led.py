
class Led:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def set(self, led: str, value: int):
        assert 0 <= value <= 255, "Value must be in 0-255 range."
        assert led in ("r", "b", "g", "bl"), \
            "Color must be 'r', 'b', 'g' or 'bl' for backlight."

        self._serial_wrapper.send(f"led {led} {value}")
    
    def red(self, value: int) -> None:
        self.set(led='r', value=value)
    
    def green(self, value: int) -> None:
        self.set(led='g', value=value)
    
    def blue(self, value: int) -> None:
        self.set(led='r', value=value)
    
    def off(self) -> None:
        self.red(value=0)
        self.green(value=0)
        self.blue(value=0)
    
    def backlight_on(self) -> None:
        self.set(led='bl', value=255)
    
    def backlight_off(self) -> None:
        self.set(led='bl', value=0)