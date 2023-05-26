from .utils import is_hexstring
from .threaded import Threaded

class Ikey(Threaded):
    KEY_TYPES_TO_KEY_DATA_LENGHT = {"Dallas": 8, "Cyfral": 2, "Metakom": 4}

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
    
    def _validations(self, key_type, key_data):
        key_types = list(self.KEY_TYPES_TO_KEY_DATA_LENGHT.keys())
        assert key_type in key_types, f"key_type must be in {key_types}"
        assert is_hexstring(key_data), "key_data must be hexstring"
        assert len(key_data.replace(' ', '')) == self.KEY_TYPES_TO_KEY_DATA_LENGHT[key_type]
        
    def read(self, timeout: int = 5) -> str:
        def _run():
            data = self._serial_wrapper.send(f"ikey read")
            #TODO: Parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    def write(self, key_type: str, key_data: str, timeout: int = 5) -> str:
        self._validations(key_type=key_type, key_data=key_data)
        def _run():
            data = self._serial_wrapper.send(f"ikey write {key_type} {key_data}")
            #TODO: Parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    def emulate(self, key_type: str, key_data: str, timeout: int = 5) -> None:
        self._validations(key_type=key_type, key_data=key_data)
        self.exec(func=None, timeout=timeout)
        self._serial_wrapper.send(f"ikey emulate {key_type} {key_data}")
