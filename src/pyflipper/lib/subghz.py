from .threaded import Threaded

class Subghz(Threaded):
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        
    def tx(self, hex_key: str, frequency: int = 433920000, te: int = 403, count: int = 10):
        # TODO: params assertion and check if default frequency is allowed worldwide
        return self._serial_wrapper.send(f"subghz tx {hex_key} {frequency} {te} {count}")

    def tx_from_file(self, file_name: str, repeat: int = 1, device: int = 0):
        assert repeat > 0
        assert device in (0, 1)  # 0 => CC1101_INT, 1 => CC1101_EXT
        return self._serial_wrapper.send(f"subghz tx_from_file {file_name} {repeat} {device}")

    def rx(self, frequency: int = 433920000, raw: bool = False, timeout: int = 5):
        # TODO: params assertion and check if default frequency is allowed worldwide
        cmd = "rx" if not raw else "rx_raw"
        def _run():
            data = self._serial_wrapper.send(f"subghz {cmd} {frequency}")
            #TODO: Parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    def decode_raw(self, sub_file: str) -> str:
        # TODO: implement regex catch errors
        assert sub_file.endswith('.sub')
        return self._serial_wrapper.send(f"subghz decode_raw {sub_file}")
    
