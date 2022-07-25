from .threaded import Threaded
from .serial_wrapper import SerialWrapper
import time

#TODO: Documentation
class Subghz(Threaded):
    def __init__(self, serial_wrapper: SerialWrapper) -> None:
        self._serial_wrapper = serial_wrapper
        self.chat = Chat(serial_wrapper=serial_wrapper)
        super().__init__()
        
        class Chat(Threaded):
            def __init__(self, serial_wrapper: SerialWrapper) -> None:
                self._serial_wrapper = serial_wrapper
                super().__init__()

            def open(self, on_message, frequency: int = 433920000):
                """
                    Chat has it's own thread, no callback nor timeout
                    On message it triggers on_message callback
                    TODO: asyncio?
                """
                def _run():
                    self._serial_wrapper.write(f"subghz chat {frequency}\r")
                    self._serial_wrapper.read_until(":")
                    while True:
                        msg = self._serial_wrapper.readline()
                        if msg:
                            #FIXME:
                            on_message(msg)
                        time.sleep(0.5)
                self.exec(func=_run, callback=None, timeout=None)

            def type(self, message: str):
                self._serial_wrapper.write(f"{message}\r")

            def close(self):
                self.stop()


    def tx(self, callback, hex_key: str, frequency: int = 433920000, count: int = 10):
        # TODO: params assertion and check if default frequency is allowed worldwide
        def _run():
            return self._serial_wrapper.send(f"subghz tx {hex_key} {frequency} {count}")
        self.exec(func=_run, callback=callback, timeout=None)

    def decode_raw(self, sub_file: str) -> str:
        # TODO: implement regex catch errors
        assert sub_file.endswith('.sub')
        return self._serial_wrapper.send(f"subghz decode_raw {sub_file}")
    
    #TODO: DEBUG CMD
    def tx_carrier(self, frequency: str):
        #tx_carrier <frequency:in Hz>     - Transmit carrier
        pass

    #TODO: DEBUG CMD
    def rx_carrier(self, frequency: str):
        #rx_carrier <frequency:in Hz>     - Receiv carrier
        pass

    #TODO: DEBUG CMD
    def encrypt_keeloq(self, path_decrypted_file: str, path_encrypted_file: str, iv: str):
        #encrypt_keeloq <path_decrypted_file> <path_encrypted_file> <IV:16 bytes in hex>  - Encrypt keeloq manufacture keys
        pass
    
    #TODO: DEBUG CMD
    def encrypt_raw(self, path_decrypted_file: str, path_encrypted_file: str, iv: str):
        #encrypt_raw <path_decrypted_file> <path_encrypted_file> <IV:16 bytes in hex>     - Encrypt RAW data
        pass
