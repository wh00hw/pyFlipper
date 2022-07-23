import re


class Bt:

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def hci_info(self):
        pattern = re.compile("(\w+):\s([\w|\d]+)")
        return {record[0]: int(record[1]) for record in pattern.findall(self._serial_wrapper.send("bt hci_info"))}
