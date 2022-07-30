class Vibro:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        
    def set(self, is_on: bool) -> None:
        assert isinstance(is_on, bool), \
            "is_on must be boolean (True or False)."
        self._serial_wrapper.send(f"vibro {1 if is_on else 0}")

    def on(self) -> None:
        self.set(is_on=True)

    def off(self) -> None:
        self.set(is_on=False)