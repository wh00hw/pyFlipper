from datetime import datetime

class Date:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def date(self) -> datetime:
        result = self._serial_wrapper.send("date")
        return datetime.strptime(result, "%Y-%m-%d %H:%M:%S %w")

    def timestamp(self) -> datetime:
        return self.date().timestamp()
    
