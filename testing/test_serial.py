import unittest
from src.pyflipper.lib import serial_wrapper


class TestSerial(unittest.TestCase):

    def test_serial_date(self):
        serial = serial_wrapper.LocalSerial("/dev/ttyACM0")

        date = serial.send("date")
        print(date)

        serial.ctrl_c()

        assert date is not None

        # 2026-05-04 13:02:30 1
        assert len(date.split(" ")) == 3



if __name__ == '__main__':
    unittest.main()

