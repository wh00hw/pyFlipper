from datetime import datetime

class Date:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def date(self) -> datetime:
        result = self._serial_wrapper.send("date")
        #FIXME: Flipper returns isoweekday 1-7 but %w is 0-6
        result = f"{result[:-1]}{int(result[-1])-1}"
        return datetime.strptime(result, "%Y-%m-%d %H:%M:%S %w")

    def timestamp(self) -> float:
        return self.date().timestamp()
    
