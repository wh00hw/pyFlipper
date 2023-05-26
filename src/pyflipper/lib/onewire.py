class Onewire:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def search(self) -> str:
        return self._serial_wrapper.send("onewire search")