import re

from .threaded import Threaded
from .utils import is_hexstring

class Ir(Threaded):
    # Fallback list used only if the protocols can't be read from `ir` help.
    PROTOCOLS = ["NEC", "NECext", "NEC42", "NEC42ext", "Samsung32",
                 "RC6", "RC5", "RC5X", "SIRC", "SIRC15", "SIRC20",
                 "Kaseikyo", "RCA", "Pioneer"]

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        self._protocols = None

    def protocols(self) -> list:
        # Read the protocol list straight from the firmware's `ir` help output
        # so it stays in sync with the installed firmware. Cached after first use.
        if self._protocols is None:
            help_text = self._serial_wrapper.send("ir")
            match = re.search(r"Available protocols:\s*(.+)", help_text)
            self._protocols = match.group(1).split() if match else list(self.PROTOCOLS)
        return self._protocols

    def tx(self, protocol: str, hex_address: str, hex_command: str) -> None:
        available = self.protocols()
        assert protocol in available, f"Available protocols: {available}"
        assert is_hexstring(hex_address), "hex_address must be hexstring"
        assert is_hexstring(hex_command), "hex_command must be hexstring"
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

