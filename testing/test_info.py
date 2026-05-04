import unittest
from src.pyflipper import PyFlipper


class TestInfo(unittest.TestCase):

    def test_info(self):
        flipper = PyFlipper(com="/dev/ttyACM0")

        # is flipper connected?
        info = flipper.device_info.info()
        print(info)

        assert info is not None

        assert info["model"] == "Flipper"



if __name__ == '__main__':
    unittest.main()

    # something
