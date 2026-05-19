import os
import unittest
from unittest import skip

from src.pyflipper import PyFlipper

# to run all tests
# python -m unittest discover -s tests -p "test_*.py" -v


class TestStorage(unittest.TestCase):

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
        info = self.flipper.storage.info("/ext")
        # print(info)

        # info is not empty
        assert info["Label"] is not None
        assert info["Type"] is not None


    def test_list(self):
        list = self.flipper.storage.list("/ext")
        # print(list)

        # list is not empty
        assert list["dirs"] is not None


    def test_read(self):
        # read file
        file = self.flipper.storage.read("/ext/Manifest") # Manifest is system-standard and thus should exist on every flipper
        # print(file)

        assert file is not None
        assert file != ""
        assert "D:subghz" in file, "File content should contain 'D:subghz'"

    def test_write_delete(self):
        file_path = "/ext/test.txt"

        # file should not exist before test
        files = self.flipper.storage.list("/ext")["files"]
        # 'files': [{'name': 'Manifest', 'size': 85176, 'weight': 'b'}, {'name': 'favorites.txt', 'size': 0, 'weight': 'b'}]
        if any(file["name"] == "test.txt" for file in files):
            self.flipper.storage.remove(file_path)

        # write new file
        self.flipper.storage.write.file(path=file_path, text="""This is a test file.""")

        # try to read the file
        files = self.flipper.storage.list("/ext")["files"]
        assert any(file["name"] == "test.txt" for file in files), "File 'test.txt' should exist after writing."

        # read file
        file = self.flipper.storage.read(file_path)
        assert file is not None
        assert file != ""
        assert "This is a test file." in file, "File content should be 'This is a test file.'"

        # remove file
        self.flipper.storage.remove(file_path)

        # try to read the file
        files = self.flipper.storage.list("/ext")["files"]
        assert all(file["name"] != "test.txt" for file in files), "File 'test.txt' should not exist after deleting."



if __name__ == '__main__':
    unittest.main()


