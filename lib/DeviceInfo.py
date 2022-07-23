import re

class DeviceInfo:

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def device_info(self):
        pattern = re.compile("([\w|_]+)\s+:\s([\w|\d]+)")
        value = {}
        for result in pattern.findall(self._serial_wrapper.send("device_info")):
            if result[1].isdigit():
                value[result[0]] = int(result[1])
            elif result[1] in ["true", "false"]:
                value[result[0]] = eval(result[1].title())
        return value       