import re


def is_hexstring(value: str) -> bool:
    try:
        int(value.replace(' ', ''), 16)
        return True
    except ValueError:
        return False


_MFC_SECTOR_COUNT = {'Mini': 5, '1K': 16, '4K': 40}


def mfc_trailer_blocks(sector_count: int):
    """Yield ``(sector, trailer_block_index)`` for a Mifare Classic layout.

    Sectors 0-31 hold 4 blocks each, sectors 32-39 (4K only) hold 16.
    """
    index = 0
    for sector in range(sector_count):
        size = 16 if sector >= 32 else 4
        yield sector, index + size - 1
        index += size


def parse_nfc(path: str):
    """Parse a Flipper native ``.nfc`` Mifare Classic dump.

    Returns ``(uid_hex, sectors)`` where ``sectors`` maps a sector number to
    ``{'A': keyA_hex, 'B': keyB_hex}``. Keys come from each sector trailer block
    (``KeyA[6] | AccessBits[4] | KeyB[6]``); ``??`` (unknown) bytes are skipped.
    """
    uid = None
    mfc_type = '1K'
    blocks = {}
    with open(path) as handle:
        for raw in handle:
            line = raw.strip()
            if line.startswith('UID:'):
                uid = line.split(':', 1)[1].replace(' ', '').upper()
            elif line.startswith('Mifare Classic type:'):
                mfc_type = line.split(':', 1)[1].strip()
            else:
                match = re.match(r'Block (\d+):\s*(.+)', line)
                if match:
                    blocks[int(match.group(1))] = match.group(2).split()

    sectors = {}
    for sector, trailer in mfc_trailer_blocks(_MFC_SECTOR_COUNT.get(mfc_type, 16)):
        data = blocks.get(trailer)
        if not data or len(data) < 16:
            continue
        entry = {}
        if '??' not in data[0:6]:
            entry['A'] = ''.join(data[0:6]).upper()
        if '??' not in data[10:16]:
            entry['B'] = ''.join(data[10:16]).upper()
        if entry:
            sectors[sector] = entry
    return uid, sectors
