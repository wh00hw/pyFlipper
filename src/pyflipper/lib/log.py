from .threaded import Threaded

class Log(Threaded):
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def attach(self, timeout: int = 10) -> str:
        self.exec(func=None, timeout=timeout)
        return self._serial_wrapper.send("log").rstrip("\r\n>:")