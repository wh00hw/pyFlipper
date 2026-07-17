from .info import Info


class Power:
    def __init__(self, serial_wrapper) -> None:
        self._serial_wrapper = serial_wrapper
        self._info = Info(serial_wrapper)

    def off(self) -> None:
        return self._serial_wrapper.send("power off")

    def reboot(self) -> None:
        return self._serial_wrapper.send("power reboot")

    def reboot2dfu(self) -> None:
        return self._serial_wrapper.send("power reboot2dfu")

    def otg_on(self) -> None:
        # Enable the 5V pin on the GPIO header.
        return self._serial_wrapper.send("power 5v 1")

    def otg_off(self) -> None:
        return self._serial_wrapper.send("power 5v 0")

    def info(self) -> dict:
        # ``power info`` was removed; power data now lives under ``info power``.
        return self._info.power_info()
