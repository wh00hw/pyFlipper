import re
from lib.Bt import Bt
from lib.DeviceInfo import DeviceInfo
from lib.Free import Free
from lib.Led import Led
from lib.Ps import Ps
from lib.SerialWrapper import SerialWrapper
from lib.Storage import Storage
from lib.Vibro import Vibro
from lib.Date import Date

class PyFlipper:

    def __init__(self, port) -> None:
        self._serial_wrapper = SerialWrapper(port=port)
        self.vibro = Vibro(serial_wrapper=self._serial_wrapper)
        self.date = Date(serial_wrapper=self._serial_wrapper)
        self.device_info = DeviceInfo(serial_wrapper=self._serial_wrapper)
        self.led = Led(serial_wrapper=self._serial_wrapper)
        self.bt = Bt(serial_wrapper=self._serial_wrapper)
        self.ps = Ps(serial_wrapper=self._serial_wrapper)
        self.free = Free(serial_wrapper=self._serial_wrapper)
        self.storage = Storage(serial_wrapper=self._serial_wrapper)