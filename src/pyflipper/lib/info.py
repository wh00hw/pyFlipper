import re


class Info:
    """Wraps the current-firmware ``info`` command family.

    ``info device`` / ``info power`` / ``info power_debug`` all print
    ``<key> : <value>`` lines (key padded to 30 columns). Values that look
    numeric or boolean are converted; everything else is kept as a string.
    """

    _PATTERN = re.compile(r"^(\S+)\s*:\s(.*)$", re.MULTILINE)

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    @staticmethod
    def _coerce(value: str):
        value = value.strip()
        if re.fullmatch(r"-?\d+", value):
            return int(value)
        if value in ("true", "false"):
            return value == "true"
        return value

    def _parse(self, command: str) -> dict:
        response = self._serial_wrapper.send(command)
        return {
            key: self._coerce(value)
            for key, value in self._PATTERN.findall(response)
        }

    def device_info(self) -> dict:
        return self._parse("info device")

    def power_info(self) -> dict:
        return self._parse("info power")

    def power_debug_info(self) -> dict:
        return self._parse("info power_debug")
