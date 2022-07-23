from curses.ascii import isdigit
import re

class Power:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def off(self):
        return self._serial_wrapper.send("power off")

    def reboot(self):
        return self._serial_wrapper.send("power reboot")
    
    def reboot2dfu(self):
        return self._serial_wrapper.send("power reboot2dfu")
    
    def info(self):
        pattern = re.compile("([\w|_]+)\s+:\s([\w|\d]+)")
        return { item[0]: int(item[1]) if item[1].isdigit() else item[1] for item in pattern.findall(self._serial_wrapper.send("power info"))}
    
