import re

class DeviceInfo:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def info(self) -> dict:
        pattern = re.compile("([\w|_]+)\s+:\s([\w|\d]+)")
        value = {}

        for x in pattern.findall(self._serial_wrapper.send("device_info")):
            if x[1].isdigit():
                value[x[0]] = int(x[1])

            elif x[1] in ["true", "false"]:
                value[x[0]] = eval(x[1].title())

            else:
                value[x[0]] = x[1]

        return value       