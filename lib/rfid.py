import re
from .threaded import Threaded
from .serial_wrapper import SerialWrapper

class RFID(Threaded):
    def __init__(self, serial_wrapper: SerialWrapper) -> None:
        self._serial_wrapper = serial_wrapper
        super().__init__()

    def read(self, callback, timeout: int = None):
        def _run():
            return self._serial_wrapper.send("rfid read").rstrip('>:')
        self.exec(func=_run, callback=callback, timeout=timeout)