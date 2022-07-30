from .threaded import Threaded

class RFID(Threaded):
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def read(self, timeout: int = 5) -> str:
        def _run():
            data = self._serial_wrapper.send("rfid read")
            #TODO: Parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()