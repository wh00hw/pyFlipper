from datetime import datetime

class Date:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def date(self):
        return datetime.strptime(self._serial_wrapper.send("date"), "%Y-%m-%d %H:%M:%S %w")

    def timestamp(self):
        return self.date().timestamp()
    