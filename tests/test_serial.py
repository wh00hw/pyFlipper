import os
import unittest
import time

from src.pyflipper.lib import serial_wrapper


class TestSerial(unittest.TestCase):
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

        self.serial = serial_wrapper.LocalSerial(com)

    # ensure close connection after every test
    def tearDown(self):
        if hasattr(self, "serial") and self.serial:
            self.serial.ctrl_c()

    def test_serial_date(self):
        date = self.serial.send("date")
        print(date)

        assert date is not None

        # 2026-05-04 13:02:30 1
        assert date != "" or date is None
        assert len(date.split(" ")) == 3

    def test_serial_storage_info(self):
        info = self.serial.send("storage info /ext")
        print(info)

        assert info is not None
        assert "Label" in info
        assert "Type" in info

    def test_serial_storage_list(self):
        list = self.serial.send("storage list /ext")
        print(list)

        assert list is not None
        # files and directories on external drive created by filesystem
        assert "[D]" in list or "[F]" in list

    def test_serial_storage_read(self):
        file = self.serial.send("storage read /ext/Manifest")
        print(file)

        assert file is not None
        assert "Size" in file

    def test_serial_storage_tree(self):
        tree = self.serial.send("storage tree /ext")
        print(tree)

        assert tree is not None
        assert "[D]" in tree or "[F]" in tree

    def test_serial_storage_stat(self):
        # system file
        stat = self.serial.send("storage stat /ext/Manifest")
        print(stat)

        assert stat is not None
        assert "File" in stat

    def test_serial_storage_write(self):
        write = self.serial.write(f"storage write /ext/test.txt\r".encode())
        # print(write)

        time.sleep(1)

        send = self.serial.write(f"this is a test file.\r".encode())
        # print(send)

        # send ctrl+c
        send = self.serial.ctrl_c()

        # check if file exists
        list = self.serial.send("storage list /ext")
        assert "test.txt" in list, "test.txt should exist in file list"

    def test_serial_storage_delete(self):
        # write new file
        self.serial.write(f"storage write /ext/test.txt\r".encode())
        self.serial.write(f"this is a test file.\r".encode())
        self.serial.ctrl_c()
        time.sleep(1)

        # check if file exists
        list = self.serial.send("storage list /ext")
        assert "test.txt" in list, "test.txt should exist in file list"

        # delete
        self.serial.write(f"storage remove /ext/test.txt\r".encode())

        # check
        list = self.serial.send("storage list /ext")
        assert "test.txt" not in list, "test.txt should not exist in file list"


if __name__ == '__main__':
    unittest.main()

