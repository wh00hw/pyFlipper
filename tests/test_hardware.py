"""Integration tests that talk to a real Flipper Zero.

These are skipped automatically when no device is connected, so the suite
still runs in CI. Force a specific port with ``FLIPPER_COM=/dev/ttyACM0``.
Run just these with:

    python -m unittest tests.test_hardware -v
"""
import os
import unittest
from datetime import datetime

from helpers import PyFlipper


def _find_flipper():
    com = os.environ.get("FLIPPER_COM")
    if com:
        return com
    dev = "/dev"
    if not os.path.isdir(dev):
        return None
    for name in sorted(os.listdir(dev)):
        if name.startswith(("ttyACM", "ttyUSB")):
            return os.path.join(dev, name)
    return None


_COM = _find_flipper()


@unittest.skipIf(_COM is None, "no Flipper connected (set FLIPPER_COM to force)")
class TestHardware(unittest.TestCase):
    def setUp(self):
        self.flipper = PyFlipper(com=_COM)

    def tearDown(self):
        sw = getattr(self, "flipper", None)
        if sw is not None:
            self.flipper._serial_wrapper.ctrl_c()
            self.flipper._serial_wrapper.close()

    def test_date(self):
        self.assertIsInstance(self.flipper.date.datetime(), datetime)

    def test_device_info(self):
        info = self.flipper.info.device_info()
        self.assertTrue(info)
        # dot-separated key on current firmware
        self.assertIn("Flipper", str(info.get("hardware.model", "")))

    def test_power_info(self):
        info = self.flipper.info.power_info()
        self.assertIn("charge.level", info)

    def test_storage_info(self):
        info = self.flipper.storage.info("/ext")
        self.assertIn("Label", info)
        self.assertIn("total_KB", info)

    def test_storage_list(self):
        listing = self.flipper.storage.list("/ext")
        self.assertIn("dirs", listing)
        self.assertIn("files", listing)

    def test_storage_write_read_delete(self):
        path = "/ext/pyflipper_test.txt"
        text = "This is a pyflipper test file."
        self.flipper.storage.write.file(text=text, path=path)
        try:
            content = self.flipper.storage.read(path)
            self.assertIn("pyflipper test file", content)
        finally:
            self.flipper.storage.remove(path)


if __name__ == "__main__":
    unittest.main()
