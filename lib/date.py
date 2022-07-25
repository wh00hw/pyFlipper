from datetime import datetime
from lib.serial_wrapper import SerialWrapper

class Date:
    def __init__(self, serial_wrapper: SerialWrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def date(self) -> datetime:
        result = self._serial_wrapper.send("date")[:-2].rstrip()
        return datetime.strptime(result, "%Y-%m-%d %H:%M:%S %w")

    def timestamp(self) -> datetime:
        return self.date().timestamp()
    