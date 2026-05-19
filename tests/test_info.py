import os
import unittest
from src.pyflipper import PyFlipper


class TestInfo(unittest.TestCase):

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

    def test_info(self):
        info = self.flipper.device_info.info()
        print(info)

        assert info is not None
        assert info["hardware_model"] == "Flipper"



if __name__ == '__main__':
    unittest.main()

    # something
