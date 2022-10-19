from .threaded import Threaded

class RFID(Threaded):
    KEY_TYPES = ["EM4100", "H10301", "Indala26", "IoProxXSF", "AWID", "FDX-A", "FDX-B", "HIDProx", "HIDExt", "Pyramid", "Viking", "Jablotron", "Paradox", "PAC/Stanley", "Keri", "Gallagher"]
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def read(self, timeout: int = 5) -> str:
        def _run():
            data = self._serial_wrapper.send("rfid read")
            #TODO: Parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    # key_type can be one of EM4100, H10301, Indala26, IoProxXSF, AWID, FDX-A, FDX-B, HIDProx, HIDExt, Pyramid, Viking, Jablotron, Paradox, PAC/Stanley, Keri, Gallagher
    # key_data is just the data you can also read from the lf rfid tags in hex eg '5500824806' from EM4100 type

    def emulate(self, key_type, key_data, timeout: int = 5) -> str:
        assert key_type in self.KEY_TYPES, f"key_type not in {str(self.KEY_TYPES)}"
        def _run():
            data = self._serial_wrapper.send("rfid emulate " + key_type + " " + key_data)
            
            return data
        self.exec(func=None, timeout=timeout)
        return _run()


    def write(self, key_type, key_data, timeout: int = 5) -> str:
        assert key_type in self.KEY_TYPES, f"key_type not in {str(self.KEY_TYPES)}"
        def _run():
            data = self._serial_wrapper.send("rfid write " + key_type + " " + key_data)
            
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    