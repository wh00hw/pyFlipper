#TODO: Documentation
class Subghz:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        
    def tx(self, hex_key: str, frequency: int = 433920000, count: int = 10):
        # TODO: params assertion and check if default frequency is allowed worldwide
        return self._serial_wrapper.send(f"subghz tx {hex_key} {frequency} {count}")

    def decode_raw(self, sub_file: str) -> str:
        # TODO: implement regex catch errors
        assert sub_file.endswith('.sub')
        return self._serial_wrapper.send(f"subghz decode_raw {sub_file}")
    