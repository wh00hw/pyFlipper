import os
import unittest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from src.pyflipper import PyFlipper

class TestDate(unittest.TestCase):

    # open new connection on every test
    def setUp(self):
        com = None
        # find out where the flipper is connected
        # get list of all connected devices
        devices = os.listdir("/dev")
        for device in devices:
            if device.startswith("ttyACM") or device.startswith("ttyUSB"):
                com = f"/dev/{device}"
                break

        if com is None:
            raise Exception("Flipper not found. Please connect your Flipper and try again.")

        self.flipper = PyFlipper(com=com)

    # close connection after every test
    def tearDown(self):
        if hasattr(self, "flipper") and self.flipper._serial_wrapper:
            self.flipper._serial_wrapper.ctrl_c()


    def test_date(self):
        date = self.flipper.date.date()
        print(date)

        assert date is not None
        assert isinstance(date, datetime)


    def test_timestamp(self):
        timestamp = self.flipper.date.timestamp()
        print(timestamp)

        assert timestamp is not None
        assert isinstance(timestamp, float)


if __name__ == '__main__':
    unittest.main()

