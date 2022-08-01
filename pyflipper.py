from lib.bt import Bt
from lib.debug import Debug
from lib.device_info import DeviceInfo
from lib.free import Free
from lib.i2c import I2c
from lib.ikey import Ikey
from lib.input import Input
from lib.ir import Ir
from lib.led import Led
from lib.log import Log
#from lib.log import Log
from lib.music_player import MusicPlayer
from lib.nfc import NFC
from lib.onewire import Onewire
from lib.ps import Ps
from lib.rfid import RFID
from lib.serial_wrapper import LocalSerial, WSSerial
from lib.storage import Storage
from lib.subghz import Subghz
from lib.vibro import Vibro
from lib.date import Date
from lib.gpio import Gpio
from lib.loader import Loader
from lib.power import Power
from lib.update import Update

class PyFlipper:

    def __init__(self, **kwargs) -> None:
        assert bool(kwargs.get('com')) ^ bool(kwargs.get('ws')), "COM or Websocket required"
        if kwargs.get('com'):
                self._serial_wrapper = LocalSerial(com=kwargs['com'])
        else:
                self._serial_wrapper = WSSerial(ws=kwargs['ws']) 
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
        self.log = Log(serial_wrapper=self._serial_wrapper)
        self.nfc = NFC(serial_wrapper=self._serial_wrapper)
        self.rfid = RFID(serial_wrapper=self._serial_wrapper)
        self.subghz = Subghz(serial_wrapper=self._serial_wrapper)
        self.ir = Ir(serial_wrapper=self._serial_wrapper)
        self.ikey = Ikey(serial_wrapper=self._serial_wrapper)
        self.debug = Debug(serial_wrapper=self._serial_wrapper)
        self.onewire = Onewire(serial_wrapper=self._serial_wrapper)
        self.i2c = I2c(serial_wrapper=self._serial_wrapper)
        self.input = Input(serial_wrapper=self._serial_wrapper)