# PyFlipper

Unoffical Flipper Zero cli wrapper written in Python

![](https://thumb.tildacdn.com/tild3332-3839-4061-b663-363464303432/-/resize/214x/-/format/webp/noroot.png)

## Articles
- [How to hack a restaurant](https://medium.com/@nic_whr/how-to-hack-a-restaurant-5d394be105a9)

## Functions and characteristics:
 - [x] Flipper serial CLI wrapper
 - [x] Websocket client interface

## Setup instructions:

```bash
$ pip install pyflipper
```
### Tested on:
 - [x] Python 3.8.10 on Linux 5.4.0 x86_64
 - [x] Python 3.9.10 on Windows 10
 - [x] Python 3.10.5 on Android 12 (Termux + [OTGSerial2WebSocket](https://play.google.com/store/apps/details?id=com.wh00hw.serial2websocket) NO ROOT REQUIRED)

## Usage/Examples

### Connection

```python
from pyflipper.pyflipper import PyFlipper

#Local serial port
flipper = PyFlipper(com="/dev/ttyACM0")

#OR 

#Remote serial2websocket server
flipper = PyFlipper(ws="ws://192.168.1.5:1337")
```
### Power

```python
#Info
info = flipper.power.info()

#Poweroff
flipper.power.off()

#Reboot
flipper.power.reboot()

#Reboot in DFU mode
flipper.power.reboot2dfu()
```
### Update/Backup

```python
#Install update from .fuf file
flipper.update.install(fuf_file="/ext/update.fuf")

#Backup Flipper to .tar file
flipper.update.backup(dest_tar_file="/ext/backup.tar")

#Restore Flipper from backup .tar file
flipper.update.restore(bak_tar_file="/ext/backup.tar")
```
### Loader

```python
#List installed apps
apps = flipper.loader.list()

#Open app
flipper.loader.open(app_name="Clock")
```

### Flipper Info

```python
#Get flipper date
date = flipper.date.date()

#Get flipper timestamp
timestamp = flipper.date.timestamp()

#Get the processes dict list
ps = flipper.ps.list()

#Get device info dict
device_info = flipper.device_info.info()

#Get heap info dict
heap = flipper.free.info()

#Get free_blocks string
free_blocks = flipper.free.blocks()

#Get bluetooth info
bt_info = flipper.bt.info()
```
### Storage

#### Filesystem Info
```python
#Get the storage filesystem info
ext_info = flipper.storage.info(fs="/ext")
```
#### Explorer
```python
#Get the storage /ext dict
ext_list = flipper.storage.list(path="/ext")

#Get the storage /ext tree dict
ext_tree = flipper.storage.tree(path="/ext")

#Get file info
file_info = flipper.storage.stat(file="/ext/foo/bar.txt")

#Make directory
flipper.storage.mkdir(new_dir="/ext/foo")
```
#### Files

```python
#Read file
plain_text = flipper.storage.read(file="/ext/foo/bar.txt")

#Remove file 
flipper.storage.remove(file="/ext/foo/bar.txt")

#Copy file 
flipper.storage.copy(src="/ext/foo/source.txt", dest="/ext/bar/destination.txt")

#Rename file 
flipper.storage.rename(file="/ext/foo/bar.txt", new_file="/ext/foo/rab.txt")

#MD5 Hash file 
md5_hash = flipper.storage.md5(file="/ext/foo/bar.txt")

#Write file in one chunk
file = "/ext/bar.txt"

text = """There are many variations of passages of Lorem Ipsum available, 
but the majority have suffered alteration in some form, by injected humour, 
or randomised words which don't look even slightly believable. 
If you are going to use a passage of Lorem Ipsum, 
you need to be sure there isn't anything embarrassing hidden in the middle of text. 
"""

flipper.storage.write.file(file, text)

#Write file using a listener
file = "/ext/foo.txt"

text_one = """There are many variations of passages of Lorem Ipsum available, 
but the majority have suffered alteration in some form, by injected humour, 
or randomised words which don't look even slightly believable. 
If you are going to use a passage of Lorem Ipsum, 
you need to be sure there isn't anything embarrassing hidden in the middle of text. 
"""

flipper.storage.write.start(file)

time.sleep(2)

flipper.storage.write.send(text_one)

text_two = """All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as 
necessary, making this the first true generator on the Internet.
 It uses a dictionary of over 200 Latin words, combined with a handful of 
 model sentence structures, to generate Lorem Ipsum which looks reasonable. 
The generated Lorem Ipsum is therefore always free from repetition, injected humour, or non-characteristic words etc.
"""
flipper.storage.write.send(text_two)

time.sleep(3)

#Don't forget to stop
flipper.storage.write.stop()
```
### LED/Backlight

```python
#Set generic led on (r,b,g,bl)
flipper.led.set(led='r', value=255)

#Set blue led off
flipper.led.blue(value=0)

#Set green led value
flipper.led.green(value=175)

#Set backlight on
flipper.led.backlight_on()

#Set backlight off
flipper.led.backlight_off()

#Turn off led
flipper.led.off()

```
### Vibro

```python
#Set vibro True or False
flipper.vibro.set(True)

#Set vibro on
flipper.vibro.on()

#Set vibro off
flipper.vibro.off()
```
### GPIO

```python
#Set gpio mode: 0 - input, 1 - output
flipper.gpio.mode(pin_name=PIN_NAME, value=1)

#Set gpio pin value: 0 - off, 1 - on
flipper.gpio.set(pin_name=PIN_NAME, value=1)

#Read gpio pin value
flipper.gpio.read(pin_name=PIN_NAME)
```

### MusicPlayer

```python
#Play song in RTTTL format
rttl_song = "Littleroot Town - Pokemon:d=4,o=5,b=100:8c5,8f5,8g5,4a5,8p,8g5,8a5,8g5,8a5,8a#5,8p,4c6,8d6,8a5,8g5,8a5,8c#6,4d6,4e6,4d6,8a5,8g5,8f5,8e5,8f5,8a5,4d6,8d5,8e5,2f5,8c6,8a#5,8a#5,8a5,2f5,8d6,8a5,8a5,8g5,2f5,8p,8f5,8d5,8f5,8e5,4e5,8f5,8g5"

#Play in loop
flipper.music_player.play(rtttl_code=rttl_song)

#Stop loop
flipper.music_player.stop()

#Play for 20 seconds
flipper.music_player.play(rtttl_code=rttl_song, duration=20)

#Beep
flipper.music_player.beep()

#Beep for 5 seconds
flipper.music_player.beep(duration=5)
```
### NFC

```python
#Synchronous default timeout 5 seconds

#Detect NFC 
nfc_detected = flipper.nfc.detect()

#Emulate NFC
flipper.nfc.emulate()

#Activate field
flipper.nfc.field()
```

### RFID

```python
#Synchronous default timeout 5 seconds

#Read RFID 
rfid = flipper.rfid.read()

#Emulate RFID 
emulated = flipper.rfid.emulate(key_type="EM4100", key_data="5500824806")

#Write RFID 
written = flipper.rfid.write(key_type="EM4100", key_data="5500824806")


```

### SubGhz

```python
#Transmit hex_key N times(default count = 10)
flipper.subghz.tx(hex_key="DEADBEEF", frequency=433920000, count=5)

#Receive (default frequency=433920000 raw=False timeout=5 seconds)
received = flipper.subghz.rx(frequency="433920000", raw=True, timeout=10)

#Decode raw .sub file
decoded = flipper.subghz.decode_raw(sub_file="/ext/subghz/foo.sub")
```
### Infrared

```python
#Transmit hex_address and hex_command selecting a protocol
flipper.ir.tx(protocol="Samsung32", hex_address="C000FFEE", hex_command="DEADBEEF")

#Raw Transmit samples
flipper.ir.tx_raw(frequency=38000, duty_cycle=0.33, samples=[1337, 8888, 3000, 5555])

#Synchronous default timeout 5 seconds
#Receive tx 
r = flipper.ir.rx(timeout=10)
```

### IKEY

```python
#Read (default timeout 5 seconds)
ikey = flipper.ikey.read()

#Write (default timeout 5 seconds)
flipper.ikey.write(key_type="Dallas", key_data="DEADBEEFCOOOFFEE")

#Emulate (default timeout 5 seconds)
flipper.ikey.emulate(key_type="Dallas", key_data="DEADBEEFCOOOFFEE")
```

### Log

```python
#Attach event logger (default timeout 10 seconds)
logs = flipper.log.attach()
```

### Debug

```python
#Activate debug mode
flipper.debug.on()

#Deactivate debug mode
flipper.debug.off()
```

### Onewire

```python
#Search
response = flipper.onewire.search()
```

### I2C

```python
#Get
response = flipper.i2c.get()
```

### Input

```python
#Input dump
dump = flipper.input.dump()

#Send input
flipper.input.send("up", "press")
```

## Optimizations

Feel free to contribute in any way

- [ ] Queue Thread orchestrator
- [ ] Implement all the cli functions
- [ ] Async SubGhz Chat

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Buy me a pint

**ZEC:** zs13zdde4mu5rj5yjm2kt6al5yxz2qjjjgxau9zaxs6np9ldxj65cepfyw55qvfp9v8cvd725f7tz7

**ETH:** 0xef3cF1Eb85382EdEEE10A2df2b348866a35C6A54

**BTC:** 15umRZXBzgUacwLVgpLPoa2gv7MyoTrKat

## Contacts

 - **Discord**: white_rabbit#4124
 - **Twitter**: @nic_whr
 - **GPG**: 0x94EDEADC
