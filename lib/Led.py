class Led:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def set(self, color, value):
        if value < 0 or value > 255:
            raise Exception("Value must be in 0-255 range")
        if color not in ["r", "b", "g", "bl"]:
            raise Exception(
                "Color must be 'r', 'g', 'g' or 'bl' for backlight")
        self._serial_wrapper.send(f"led {color} {value}")