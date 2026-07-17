"""Command-level tests against simulated current-firmware CLI output.

Sample outputs mirror the exact formats printed by firmware 1.4.3 / dev
(see the source files cited in the project notes).
"""
import unittest
from datetime import datetime

from helpers import FakeFlipperTestCase


class TestDate(FakeFlipperTestCase):
    def test_datetime_parsing(self):
        flipper, _ = self.make_flipper({"date": "2026-05-04 13:02:30 1"})
        dt = flipper.date.datetime()
        self.assertEqual(dt, datetime(2026, 5, 4, 13, 2, 30))

    def test_timestamp(self):
        flipper, _ = self.make_flipper({"date": "2026-05-04 13:02:30 1"})
        self.assertIsInstance(flipper.date.timestamp(), float)

    def test_date_alias(self):
        flipper, _ = self.make_flipper({"date": "2026-05-04 13:02:30 1"})
        self.assertEqual(flipper.date.date(), flipper.date.datetime())


class TestInfo(FakeFlipperTestCase):
    DEVICE = (
        "hardware.model                : Flipper\r\n"
        "hardware.name                 : Zero\r\n"
        "firmware.version              : 1.4.3\r\n"
        "firmware.build_date           : 12-12-2025\r\n"
        "radio.alive                   : true"
    )
    POWER = (
        "charge.level                  : 87\r\n"
        "charge.state                  : discharging\r\n"
        "battery.voltage               : 4056\r\n"
        "battery.current               : -12\r\n"
        "battery.temp                  : 27"
    )

    def test_device_info(self):
        flipper, port = self.make_flipper({"info device": self.DEVICE})
        info = flipper.info.device_info()
        self.assert_sent(port, "info device")
        self.assertEqual(info["hardware.model"], "Flipper")
        self.assertEqual(info["firmware.version"], "1.4.3")
        self.assertIs(info["radio.alive"], True)

    def test_power_info(self):
        flipper, port = self.make_flipper({"info power": self.POWER})
        info = flipper.info.power_info()
        self.assert_sent(port, "info power")
        self.assertEqual(info["charge.level"], 87)
        self.assertEqual(info["battery.current"], -12)  # signed
        self.assertEqual(info["charge.state"], "discharging")

    def test_power_debug_info_command(self):
        flipper, port = self.make_flipper({"info power_debug": "gauge.vbat : 4056"})
        flipper.info.power_debug_info()
        self.assert_sent(port, "info power_debug")

    def test_power_module_info_delegates(self):
        flipper, port = self.make_flipper({"info power": self.POWER})
        info = flipper.power.info()
        self.assert_sent(port, "info power")
        self.assertEqual(info["charge.level"], 87)


class TestStorage(FakeFlipperTestCase):
    def test_info_kib(self):
        flipper, port = self.make_flipper({
            "storage info /ext":
                "Label: SD_CARD\r\nType: FAT32\r\n30528KiB total\r\n28880KiB free",
        })
        info = flipper.storage.info("/ext")
        self.assert_sent(port, "storage info /ext")
        self.assertEqual(info["Label"], "SD_CARD")
        self.assertEqual(info["Type"], "FAT32")
        self.assertEqual(info["total_KB"], 30528)
        self.assertEqual(info["free_KB"], 28880)

    def test_info_issue_21_exfat_kib_empty_label(self):
        # Regression for issue #21: exFAT card, "KiB" units, empty label.
        flipper, _ = self.make_flipper({
            "storage info /ext": (
                "Label: \r\nType: EXFAT\r\n62302208KiB total\r\n"
                "61031936KiB free\r\n03SD SD64G v8.5\r\nSN:fabbeae8 03/2023"
            ),
        })
        info = flipper.storage.info("/ext")
        self.assertEqual(info["Type"], "EXFAT")
        self.assertEqual(info["total_KB"], 62302208)
        self.assertEqual(info["free_KB"], 61031936)

    def test_info_rejects_bad_fs(self):
        flipper, _ = self.make_flipper()
        with self.assertRaises(AssertionError):
            flipper.storage.info("/bad")

    def test_list(self):
        flipper, port = self.make_flipper({
            "storage list /ext":
                "\t[D] subghz\r\n\t[D] nfc\r\n\t[F] Manifest 85176b\r\n\t[F] update.log 12b",
        })
        listing = flipper.storage.list("/ext")
        self.assert_sent(port, "storage list /ext")
        self.assertEqual(listing["dirs"], ["subghz", "nfc"])
        self.assertEqual(listing["files"][0],
                         {"name": "Manifest", "size": 85176, "weight": "b"})
        self.assertEqual(listing["files"][1]["size"], 12)

    def test_read_multiline(self):
        flipper, port = self.make_flipper({
            "storage read /ext/notes.txt":
                "Size: 22\r\nfirst line\r\nsecond line",
        })
        content = flipper.storage.read("/ext/notes.txt")
        self.assert_sent(port, "storage read /ext/notes.txt")
        self.assertEqual(content, "first line\nsecond line")

    def test_stat(self):
        flipper, port = self.make_flipper(
            {"storage stat /ext/a": "File, size: 22b"})
        self.assertEqual(flipper.storage.stat("/ext/a"), "File, size: 22b")

    def test_mkdir_remove_commands(self):
        flipper, port = self.make_flipper({"storage mkdir /ext/foo": "",
                                           "storage remove /ext/foo": ""})
        flipper.storage.mkdir("/ext/foo")
        flipper.storage.remove("/ext/foo")
        self.assert_sent(port, "storage mkdir /ext/foo")
        self.assert_sent(port, "storage remove /ext/foo")


class TestBt(FakeFlipperTestCase):
    def test_hci_info_command(self):
        flipper, port = self.make_flipper(
            {"bt hci_info": "advertising: 1\r\nconnected: 0"})
        info = flipper.bt.info()
        self.assert_sent(port, "bt hci_info")
        self.assertEqual(info, {"advertising": 1, "connected": 0})


class TestFree(FakeFlipperTestCase):
    def test_free_parses_first_fields(self):
        flipper, port = self.make_flipper({
            "free": ("Free heap size: 100000\r\nTotal heap size: 200000\r\n"
                     "Minimum heap size: 90000\r\nMaximum heap block: 50000\r\n"
                     "Pool free: 4096\r\nMaximum pool block: 2048"),
        })
        info = flipper.free.info()
        self.assertEqual(info["free_heap_size"], 100000)
        self.assertEqual(info["total_heap_size"], 200000)


class TestSimpleCommands(FakeFlipperTestCase):
    def test_led(self):
        flipper, port = self.make_flipper({"led r 255": ""})
        flipper.led.red(255)
        self.assert_sent(port, "led r 255")

    def test_led_validates_range(self):
        flipper, _ = self.make_flipper()
        with self.assertRaises(AssertionError):
            flipper.led.set("r", 300)

    def test_vibro(self):
        flipper, port = self.make_flipper({"vibro 1": "", "vibro 0": ""})
        flipper.vibro.on()
        flipper.vibro.off()
        self.assert_sent(port, "vibro 1")
        self.assert_sent(port, "vibro 0")

    def test_debug_uses_sysctl(self):
        flipper, port = self.make_flipper({"sysctl debug 1": "",
                                           "sysctl debug 0": ""})
        flipper.debug.on()
        flipper.debug.off()
        self.assert_sent(port, "sysctl debug 1")
        self.assert_sent(port, "sysctl debug 0")

    def test_gpio(self):
        flipper, port = self.make_flipper({"gpio set pa7 1": ""})
        flipper.gpio.set("pa7", 1)
        self.assert_sent(port, "gpio set pa7 1")

    def test_power_reboot(self):
        flipper, port = self.make_flipper({"power reboot": ""})
        flipper.power.reboot()
        self.assert_sent(port, "power reboot")


class TestSubghz(FakeFlipperTestCase):
    def test_tx_includes_device_arg(self):
        flipper, port = self.make_flipper(
            {"subghz tx AABBCC 433920000 403 10 0": ""})
        flipper.subghz.tx("AABBCC")
        self.assert_sent(port, "subghz tx AABBCC 433920000 403 10 0")

    def test_rx_includes_device_arg(self):
        flipper, port = self.make_flipper(
            {"subghz rx 433920000 0": "captured"})
        flipper.subghz.rx(timeout=1)
        self.assert_sent(port, "subghz rx 433920000 0")

    def test_tx_rejects_bad_device(self):
        flipper, _ = self.make_flipper()
        with self.assertRaises(AssertionError):
            flipper.subghz.tx("AABBCC", device=5)


class TestIr(FakeFlipperTestCase):
    HELP = ("Usage:\r\n\tir rx [raw]\r\n\tir tx <protocol> <address> <command>\r\n"
            "\tAvailable protocols: NEC NECext NEC42 Samsung32 RC6 Pioneer\r\n"
            "\tRaw format:\r\n")

    def test_protocols_parsed_from_help(self):
        flipper, port = self.make_flipper({"ir": self.HELP})
        self.assertEqual(
            flipper.ir.protocols(),
            ["NEC", "NECext", "NEC42", "Samsung32", "RC6", "Pioneer"],
        )

    def test_tx_accepts_firmware_protocol(self):
        flipper, port = self.make_flipper(
            {"ir": self.HELP, "ir tx Pioneer 00 01": ""})
        flipper.ir.tx("Pioneer", "00", "01")
        self.assert_sent(port, "ir tx Pioneer 00 01")

    def test_tx_rejects_unknown_protocol(self):
        flipper, _ = self.make_flipper({"ir": self.HELP})
        with self.assertRaises(AssertionError):
            flipper.ir.tx("BOGUS", "00", "01")


class TestNFC(FakeFlipperTestCase):
    def _flipper(self, nfc_responses):
        return self.make_flipper(subshells={"nfc": nfc_responses})

    def test_scan_parses_protocol(self):
        flipper, port = self._flipper({
            "scanner": "Press Ctrl+C to abort\r\n\r\nProtocols detected: Mifare Classic",
        })
        result = flipper.nfc.scan(timeout=0.2)
        self.assertEqual(result["protocols"], ["Mifare Classic"])
        # Verify the sub-shell was entered, driven and left.
        self.assertIn(b"nfc\r", port.written)
        self.assertIn(b"scanner\r", port.written)
        self.assertIn(b"exit\r", port.written)

    def test_scan_none_when_nothing_detected(self):
        flipper, _ = self._flipper({"scanner": "Press Ctrl+C to abort"})
        self.assertIsNone(flipper.nfc.scan(timeout=0.2))

    def test_detect_alias(self):
        flipper, port = self._flipper(
            {"scanner": "Protocols detected: NTAG/Ultralight"})
        result = flipper.nfc.detect(timeout=0.2)
        self.assertEqual(result["protocols"], ["NTAG/Ultralight"])

    def test_dump_builds_command(self):
        flipper, port = self._flipper({
            "dump -p mfc -f /ext/nfc/t.nfc -t 2000": "Dumping...\r\nSuccess",
        })
        flipper.nfc.dump(file="/ext/nfc/t.nfc", protocol="mfc", timeout=2000)
        self.assertIn(b"dump -p mfc -f /ext/nfc/t.nfc -t 2000\r", port.written)

    def test_dump_rejects_bad_protocol(self):
        flipper, _ = self._flipper({})
        with self.assertRaises(AssertionError):
            flipper.nfc.dump(protocol="Mifare Classic")

    def test_mfu_read_block_command(self):
        flipper, port = self._flipper({"mfu rdbl -b 4": "Block 4: 00 01 02 03"})
        out = flipper.nfc.mfu_read_block(4)
        self.assertIn(b"mfu rdbl -b 4\r", port.written)
        self.assertIn("00 01 02 03", out)

    def test_apdu_joins_payloads(self):
        flipper, port = self._flipper({'apdu -d "00A4 0400"': "9000"})
        flipper.nfc.apdu(["00A4", "0400"])
        self.assertIn(b'apdu -d "00A4 0400"\r', port.written)


class TestNFCKeyCache(FakeFlipperTestCase):
    # A Flipper .nfc dump with entirely fictional keys (no real card data).
    NFC_DUMP = (
        "Filetype: Flipper NFC device\n"
        "Version: 3\n"
        "Device type: Mifare Classic\n"
        "UID: DE AD BE EF\n"
        "ATQA: 00 04\n"
        "SAK: 08\n"
        "Mifare Classic type: 1K\n"
        "Block 0: DE AD BE EF 11 08 04 00 62 63 64 65 66 67 68 69\n"
        "Block 1: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
        "Block 2: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
        "Block 3: FF FF FF FF FF FF FF 07 80 69 A1 A2 A3 A4 A5 A6\n"
        "Block 4: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
        "Block 5: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
        "Block 6: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00\n"
        "Block 7: 11 22 33 44 55 66 FF 07 80 69 66 55 44 33 22 11\n"
    )

    def _write_nfc(self):
        import tempfile
        path = tempfile.mktemp(suffix=".nfc")
        with open(path, "w") as fh:
            fh.write(self.NFC_DUMP)
        return path

    def test_parse_nfc(self):
        from pyflipper.lib.utils import parse_nfc
        uid, sectors = parse_nfc(self._write_nfc())
        self.assertEqual(uid, "DEADBEEF")
        self.assertEqual(sectors[0], {"A": "FFFFFFFFFFFF", "B": "A1A2A3A4A5A6"})
        self.assertEqual(sectors[1], {"A": "112233445566", "B": "665544332211"})

    def test_parse_nfc_skips_unknown_keys(self):
        from pyflipper.lib.utils import parse_nfc
        dump = self.NFC_DUMP.replace(
            "Block 7: 11 22 33 44 55 66 FF 07 80 69 66 55 44 33 22 11",
            "Block 7: ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ?? ??")
        import tempfile
        path = tempfile.mktemp(suffix=".nfc")
        with open(path, "w") as fh:
            fh.write(dump)
        uid, sectors = parse_nfc(path)
        self.assertIn(0, sectors)
        self.assertNotIn(1, sectors)  # unknown trailer skipped

    def test_build_key_cache_format(self):
        flipper, _ = self.make_flipper()
        content = flipper.nfc.build_key_cache(
            "DEADBEEF", {0: {"A": "FFFFFFFFFFFF", "B": "A1A2A3A4A5A6"}})
        self.assertIn("Filetype: Flipper NFC keys", content)
        self.assertIn("Mifare Classic type: 1K", content)
        self.assertIn("Key A map: 0000000000000001", content)
        self.assertIn("Key A sector 0: FF FF FF FF FF FF", content)
        self.assertIn("Key B sector 0: A1 A2 A3 A4 A5 A6", content)

    def test_import_nfc_keys_writes_cache(self):
        flipper, port = self.make_flipper()
        uid, path = flipper.nfc.import_nfc_keys(self._write_nfc())
        self.assertEqual(uid, "DEADBEEF")
        self.assertEqual(path, "/ext/nfc/.cache/DEADBEEF.keys")
        written = b"".join(port.written)
        self.assertIn(b"storage write /ext/nfc/.cache/DEADBEEF.keys\r", written)
        self.assertIn(b"Key A sector 1: 11 22 33 44 55 66", written)


class TestLoader(FakeFlipperTestCase):
    def test_open_command(self):
        flipper, port = self.make_flipper({"loader open Clock": ""})
        flipper.loader.open("Clock")
        self.assert_sent(port, "loader open Clock")


if __name__ == "__main__":
    unittest.main()
