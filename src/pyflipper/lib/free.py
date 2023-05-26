import re

class Free:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def info(self) -> dict:
        pattern = re.compile("([\w|\s]+):\s(\d+)")
        return {result[0].lower().replace(" ", "_").strip(): int(result[1]) for result in pattern.findall(self._serial_wrapper.send("free"))}
    
    def blocks(self) -> str:
        return self._serial_wrapper.send("free_blocks")