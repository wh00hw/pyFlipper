def is_hexstring(value: str) -> bool:
    try:
        int(value.replace(' ', ''), 16)
        return True
    except ValueError:
        return False