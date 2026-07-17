class Debug:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def on(self) -> None:
        # Standalone ``debug`` was folded into ``sysctl`` in current firmware.
        self._serial_wrapper.send("sysctl debug 1")

    def off(self) -> None:
        self._serial_wrapper.send("sysctl debug 0")