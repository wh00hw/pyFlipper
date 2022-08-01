class I2c:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def get(self) -> str:
        return self._serial_wrapper.send("i2c")