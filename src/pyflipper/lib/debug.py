class Debug:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def on(self) -> None:
        self._serial_wrapper.send("debug 1")

    def off(self) -> None:
        self._serial_wrapper.send("debug 0")