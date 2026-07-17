from datetime import datetime


class Date:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def datetime(self) -> datetime:
        # Firmware prints "YYYY-MM-DD HH:MM:SS W" where W is the ISO weekday
        # (1=Mon..7=Sun). We only need the date/time part to build a datetime.
        result = self._serial_wrapper.send("date").strip()
        date_part = result.rsplit(" ", 1)[0]
        return datetime.strptime(date_part, "%Y-%m-%d %H:%M:%S")

    # Backwards-compatible alias.
    def date(self) -> datetime:
        return self.datetime()

    def timestamp(self) -> float:
        return self.datetime().timestamp()
