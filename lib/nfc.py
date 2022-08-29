import re
from .threaded import Threaded

class NFC(Threaded):
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def detect(self, timeout: int = 5) -> dict:
        def _run():
            p = re.compile(
                "found:\s([A-Z|\-]+)\sUID\slength:\s(\d+),\sUID:([\w|\d]+)")
            try:
                x = re.search(p, self._serial_wrapper.send("nfc detect")).groups()
                return {'type': x[0], 'lenght': x[1], 'UID': x[2]}
            except Exception:
                return None
        self.exec(func=None, timeout=timeout)
        return _run()

    def emulate(self, timeout: int = 5) -> None:
        def _run() -> str:
            data = self._serial_wrapper.send("nfc emulate")
            #TODO parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    def field(self, timeout: int = 5) -> None:
        def _run() -> str:
            data = self._serial_wrapper.send("nfc field")
            #TODO parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()
