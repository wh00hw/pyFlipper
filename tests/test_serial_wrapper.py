"""Transport-layer tests: echo/prompt stripping, ANSI handling, error raising."""
import unittest

from helpers import serial_wrapper, FakeFlipperTestCase
from fake_serial import FakeSerialPort


class TestCleanResponse(unittest.TestCase):
    def test_strips_echo_and_prompt(self):
        raw = "date\r\n2026-05-04 13:02:30 1\r\n>:"
        self.assertEqual(
            serial_wrapper._clean_response(raw, "date"),
            "2026-05-04 13:02:30 1",
        )

    def test_preserves_multiline_body(self):
        raw = "storage read /ext/a\r\nSize: 11\r\nhello\r\nworld\r\n>:"
        self.assertEqual(
            serial_wrapper._clean_response(raw, "storage read /ext/a"),
            "Size: 11\r\nhello\r\nworld",
        )

    def test_strips_ansi_escape_codes(self):
        raw = "date\x1b[1D\r\n\x1b[0m2026-05-04 13:02:30 1\r\n>:"
        self.assertEqual(
            serial_wrapper._clean_response(raw, "date"),
            "2026-05-04 13:02:30 1",
        )

    def test_no_echo_present(self):
        raw = "just output\r\n>:"
        self.assertEqual(
            serial_wrapper._clean_response(raw, "date"),
            "just output",
        )


class TestLocalSerialRoundTrip(FakeFlipperTestCase):
    def test_send_returns_clean_output(self):
        flipper, port = self.make_flipper({"date": "2026-05-04 13:02:30 1"})
        self.assertEqual(flipper._serial_wrapper.send("date"),
                         "2026-05-04 13:02:30 1")
        self.assert_sent(port, "date")

    def test_error_output_raises(self):
        flipper, port = self.make_flipper(
            {"storage read /ext/nope": "Storage error: file not found"})
        with self.assertRaises(Exception):
            flipper._serial_wrapper.send("storage read /ext/nope")

    def test_banner_consumed_on_connect(self):
        # A fresh connection must not leak the welcome banner into the first send.
        flipper, port = self.make_flipper({"vibro 1": ""})
        self.assertEqual(flipper._serial_wrapper.send("vibro 1"), "")


if __name__ == "__main__":
    unittest.main()
