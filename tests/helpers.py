"""Shared helpers for the hardware-free test suite."""
import os
import sys
import unittest
from unittest import mock

# Make the in-tree package importable without installing it.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fake_serial import FakeSerialPort  # noqa: E402
import pyflipper.lib.serial_wrapper as serial_wrapper  # noqa: E402
from pyflipper import PyFlipper  # noqa: E402


class FakeFlipperTestCase(unittest.TestCase):
    """Base class that wires a PyFlipper up to a simulated serial port."""

    def make_flipper(self, responses=None, subshells=None):
        port = FakeSerialPort(responses or {}, subshells=subshells)
        patcher = mock.patch.object(serial_wrapper.serial, "Serial",
                                    return_value=port)
        patcher.start()
        self.addCleanup(patcher.stop)
        flipper = PyFlipper(com="/dev/fake")
        return flipper, port

    def assert_sent(self, port, command):
        """Assert the exact CLI command (``<cmd>\\r``) was written."""
        self.assertIn(f"{command}\r".encode(), port.written,
                      msg=f"{command!r} not in {port.written!r}")
