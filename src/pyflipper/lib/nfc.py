import re

from .storage import Storage
from .utils import parse_nfc


class NFC:
    """Drives the current-firmware NFC command-line sub-shell.

    On current Flipper firmware (stock NFC CLI, PR #4158+) ``nfc`` opens an
    interactive sub-shell with the commands ``scanner``, ``dump``, ``emulate``,
    ``field``, ``apdu``, ``raw`` and ``mfu``. This class enters that sub-shell,
    runs a single command and leaves again, so each public method is a normal
    blocking call.
    """

    # The sub-shell prompt is "[nfc]>: "; both it and the top-level ">: " end
    # in ">:" which the transport layer already reads up to.
    _PROMPT_MARKER = b">:"

    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper

    # -- sub-shell plumbing ---------------------------------------------
    def _enter(self) -> None:
        self._serial_wrapper.write(b"nfc\r")
        self._serial_wrapper.read_until_prompt()

    def _leave(self) -> None:
        self._serial_wrapper.write(b"exit\r")
        self._serial_wrapper.read_until_prompt()

    @staticmethod
    def _clean(raw: str, command: str) -> str:
        marker = f"{command}\r\n"
        if marker in raw:
            raw = raw.split(marker, 1)[1]
        elif raw.startswith(command):
            raw = raw[len(command):]
        raw = raw.rstrip()
        for prompt in ("[nfc]>:", ">:"):
            if raw.endswith(prompt):
                raw = raw[: -len(prompt)]
                break
        return raw.strip()

    def _run(self, command: str, max_seconds: float = 8.0) -> str:
        """Run a command that returns to the prompt on its own."""
        self._enter()
        try:
            self._serial_wrapper.write(f"{command}\r".encode())
            raw = self._serial_wrapper.capture(max_seconds, marker=self._PROMPT_MARKER)
        finally:
            self._leave()
        return self._clean(raw, command)

    def _run_timed(self, command: str, seconds: float) -> str:
        """Run a continuous command (scanner/field/emulate) for `seconds`."""
        self._enter()
        try:
            self._serial_wrapper.write(f"{command}\r".encode())
            raw = self._serial_wrapper.capture(seconds)
            self._serial_wrapper.ctrl_c()
            self._serial_wrapper.read_until_prompt()
        finally:
            self._leave()
        return self._clean(raw, command)

    # -- commands -------------------------------------------------------
    def scan(self, timeout: int = 5, tree: bool = False) -> dict:
        """Detect the tag type. Returns {'protocols': [...]} or None if none."""
        out = self._run_timed(f"scanner{' -t' if tree else ''}", seconds=timeout)
        match = re.search(r"Protocols detected:\s*(.+)", out)
        if not match:
            return None
        protocols = [p.strip() for p in re.split(r",|\r?\n", match.group(1)) if p.strip()]
        return {'protocols': protocols, 'raw': out}

    # Backwards-compatible alias for the old flat `nfc detect`.
    def detect(self, timeout: int = 5) -> dict:
        return self.scan(timeout=timeout)

    # Protocol tokens accepted by the `dump`/`-p` argument (firmware names).
    PROTOCOLS = ("14_3a", "14_3b", "14_4a", "14_4b", "15", "felica", "mfu",
                 "mfc", "mfp", "des", "slix", "st25", "ntag4", "t4t")

    def dump(self, file: str = None, protocol: str = None, key: str = None,
             timeout: int = 5000) -> str:
        """Dump a tag to a .nfc file on the Flipper.

        `protocol` is a firmware token (e.g. "mfc" for Mifare Classic, "mfu"
        for Ultralight — see `NFC.PROTOCOLS`); if omitted the tag type is
        auto-detected. `key` is only used by protocols that authenticate via a
        single key (Mifare Ultralight, 4 or 16 byte). Mifare Classic keys come
        from the per-UID key cache (see `import_nfc_keys`), not this argument.
        """
        if protocol and protocol not in self.PROTOCOLS:
            raise AssertionError(f"protocol must be one of {self.PROTOCOLS}")
        cmd = "dump"
        if key:
            cmd += f" -k {key}"
        if protocol:
            cmd += f" -p {protocol}"
        if file:
            cmd += f" -f {file}"
        cmd += f" -t {timeout}"
        # Give the command its full timeout (ms) plus margin to finish.
        return self._run(cmd, max_seconds=timeout / 1000 + 3)

    def emulate(self, file: str, timeout: int = 10) -> str:
        """Emulate a stored .nfc file for `timeout` seconds."""
        return self._run_timed(f"emulate -f {file}", seconds=timeout)

    def field(self, timeout: int = 5) -> str:
        """Turn the NFC field on for `timeout` seconds."""
        return self._run_timed("field", seconds=timeout)

    def apdu(self, data, protocol: str = None) -> str:
        """Send APDU payload(s) to an ISO14443-4 / ISO15693-3 tag.

        `data` is a hex payload string (or a list of them). Firmware format is
        space-separated payloads: "p1 p2 p3".
        """
        if isinstance(data, (list, tuple)):
            data = " ".join(data)
        cmd = "apdu"
        if protocol:
            cmd += f" -p {protocol}"
        cmd += f' -d "{data}"'
        return self._run(cmd)

    def raw(self, data, protocol: str = None, crc: bool = False,
            keep_field: bool = False, select: bool = False,
            timeout: int = None) -> str:
        """Send raw bytes (hex) using the selected low-level protocol."""
        cmd = "raw"
        if timeout is not None:
            cmd += f" -t {timeout}"
        if keep_field:
            cmd += " -k"
        if crc:
            cmd += " -c"
        if select:
            cmd += " -s"
        if protocol:
            cmd += f" -p {protocol}"
        cmd += f' -d "{data}"'
        return self._run(cmd)

    def mfu_info(self) -> str:
        """Read basic info from a Mifare Ultralight card."""
        return self._run("mfu info")

    def mfu_read_block(self, block: int) -> str:
        return self._run(f"mfu rdbl -b {block}")

    def mfu_write_block(self, block: int, data: str) -> str:
        return self._run(f"mfu wrbl -b {block} -d {data}")

    # -- Mifare Classic key cache ---------------------------------------
    # The CLI `dump` reads Mifare Classic keys from a per-UID cache file, NOT
    # from the key dictionaries. These helpers create that cache so a card with
    # known keys can be dumped over the CLI.
    KEY_CACHE_DIR = "/ext/nfc/.cache"
    _MFC_TYPE_BY_SECTORS = {5: "Mini", 16: "1K", 40: "4K"}

    @staticmethod
    def _format_key(key: str) -> str:
        key = key.replace(" ", "").upper()
        return " ".join(key[i:i + 2] for i in range(0, len(key), 2))

    def build_key_cache(self, uid: str, sectors: dict, mfc_type: str = None) -> str:
        """Build the flipper-format ``.keys`` cache text for a Mifare Classic.

        `sectors` maps a sector number to ``{'A': keyA_hex, 'B': keyB_hex}``.
        Returns the file content (does not touch the device).
        """
        sector_count = max(sectors) + 1
        if mfc_type is None:
            mfc_type = self._MFC_TYPE_BY_SECTORS.get(sector_count, "1K")

        key_a_mask = key_b_mask = 0
        for sector, keys in sectors.items():
            if keys.get("A"):
                key_a_mask |= (1 << sector)
            if keys.get("B"):
                key_b_mask |= (1 << sector)

        lines = [
            "Filetype: Flipper NFC keys",
            "Version: 1",
            f"Mifare Classic type: {mfc_type}",
            f"Key A map: {key_a_mask:016X}",
            f"Key B map: {key_b_mask:016X}",
        ]
        for sector in sorted(sectors):
            if sectors[sector].get("A"):
                lines.append(f"Key A sector {sector}: {self._format_key(sectors[sector]['A'])}")
            if sectors[sector].get("B"):
                lines.append(f"Key B sector {sector}: {self._format_key(sectors[sector]['B'])}")
        return "\n".join(lines) + "\n"

    def write_key_cache(self, uid: str, sectors: dict, mfc_type: str = None) -> str:
        """Write the per-UID Mifare Classic key cache to the Flipper.

        Returns the on-device path of the cache file.
        """
        uid = uid.replace(" ", "").upper()
        content = self.build_key_cache(uid, sectors, mfc_type=mfc_type)
        path = f"{self.KEY_CACHE_DIR}/{uid}.keys"
        storage = Storage(self._serial_wrapper)
        try:
            storage.mkdir(self.KEY_CACHE_DIR)
        except Exception:
            pass  # directory already exists
        storage.write.file(text=content, path=path)
        return path

    def import_nfc_keys(self, nfc_path: str, mfc_type: str = None) -> tuple:
        """Load keys from a Flipper ``.nfc`` dump into the per-UID key cache.

        Returns ``(uid, cache_path)``. After this, ``dump()`` can read the card
        over the CLI. Only sectors whose keys are present in the dump are added.
        """
        uid, sectors = parse_nfc(nfc_path)
        if not uid:
            raise ValueError("could not determine UID from .nfc file")
        if not sectors:
            raise ValueError("no keys found in .nfc file")
        return uid, self.write_key_cache(uid, sectors, mfc_type=mfc_type)
