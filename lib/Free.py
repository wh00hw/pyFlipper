import re

class Free:

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def free(self):
        pattern = re.compile("([\w|\s]+):\s(\d+)")
        return { result[0].strip(): int(result[1]) for result in pattern.findall(self._serial_wrapper.send("free")) }