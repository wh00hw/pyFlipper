from .threaded import Threaded
from .utils import is_hexstring

class Ir(Threaded):
    # TODO: auto parse available protocols from >: ir help
    PROTOCOLS = ["NEC", "NEC42", "NEC42ext", "Samsung32",
                 "RC6", "RC5", "RC5X", "SIRC", "SIRC15", "SIRC20"]

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    def tx(self, protocol: str, hex_address: str, hex_command: str) -> None:
        assert protocol in self.PROTOCOLS, f"Available protocols: {self.PROTOCOLS}"
        assert is_hexstring(hex_address), "hex_address must be hexstring"
        assert is_hexstring(hex_command), "hex_command must be hexstring"
        assert len(hex_address.replace(' ', '')) == 8 and len(hex_command.replace(
            ' ', '')) == 8, "hex_address and hex_command must be 4 bytes long each"
        address = ' '.join(hex_address[i:i+2] for i in range(0, len(hex_address), 2)) if " " not in hex_address else hex_address
        command = ' '.join(hex_command[i:i+2] for i in range(0, len(hex_command), 2)) if " " not in hex_command else hex_command
        self._serial_wrapper.send(f"ir tx {protocol} {address} {command}")

    def rx(self, timeout: int = 5) -> str:
        def _run() -> str:
            data = self._serial_wrapper.send("ir rx")
            # TODO parse data
            return data
        self.exec(func=None, timeout=timeout)
        return _run()

    def tx_raw(self, frequency:int , duty_cycle: float, samples: list or str) -> None:
        assert frequency > 10000 and frequency < 56000, "Frequency must be in range (10000 - 56000)"
        assert duty_cycle >= 0.0 and duty_cycle <= 1.0, "Duty cycle must be in range (0.0 - 1.0)"
        if isinstance(samples, list):
            samples = " ".join(list(map(lambda x: str(x), samples)))
        self._serial_wrapper.send(f"ir tx RAW F:{frequency} DC:{int(duty_cycle*100)} {samples}")

