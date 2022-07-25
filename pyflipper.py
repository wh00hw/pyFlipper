from lib.rfid import RFID
from lib.bt import Bt
from lib.device_info import DeviceInfo
from lib.free import Free
from lib.led import Led
#from lib.log import Log
from lib.music_player import MusicPlayer
from lib.nfc import NFC
from lib.ps import Ps
from lib.serial_wrapper import SerialWrapper
from lib.storage import Storage
from lib.subghz import Subghz
from lib.vibro import Vibro
from lib.date import Date
from lib.gpio import Gpio
from lib.loader import Loader
from lib.power import Power
from lib.update import Update

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
        self.gpio = Gpio(serial_wrapper=self._serial_wrapper)
        self.loader = Loader(serial_wrapper=self._serial_wrapper)
        self.music_player = MusicPlayer(serial_wrapper=self._serial_wrapper)
        self.power = Power(serial_wrapper=self._serial_wrapper)
        self.update = Update(serial_wrapper=self._serial_wrapper)
#        self.log = Log(serial_wrapper=self._serial_wrapper)
        self.nfc = NFC(serial_wrapper=self._serial_wrapper)
        self.rfid = RFID(serial_wrapper=self._serial_wrapper)
        self.subghz = Subghz(serial_wrapper=self._serial_wrapper)
