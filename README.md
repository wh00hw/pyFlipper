# PyFlipper

Unoffical Flipper Zero cli wrapper written in Python

## Installation

Install PyFlipper with pip

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```
## Usage/Examples

### Connection

```python
from pyflipper import PyFlipper

#Instantiate flipper object with the correct serial port
flipper = PyFlipper("/dev/ttyACM0")
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
flipper.update.install("/ext/update.fuf")

#Backup Flipper to .tar file
flipper.update.install("/ext/backup.tar")

#Restore Flipper from backup .tar file
flipper.update.restore("/ext/backup.tar")
```
### Loader

```python
#List installed apps
apps = flipper.loader.list()

#Open an app
flipper.loader.open("Music Player")
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

#Get bluetooth info
bt_info = flipper.bt.info()
```
### Storage

#### Filesystem Info
```python
#Get the storage filesystem info
ext_info = flipper.storage.info('/ext')
```
#### Explorer
```python
#Get the storage /ext list
ext_list = flipper.storage.list('/ext')

#Get the storage /ext tree
ext_tree = flipper.storage.tree('/ext')

#Get file info
file_info = flipper.storage.stat("/ext/foo/bar.txt")

#Make directory
file_info = flipper.storage.mkdir("/ext/foo")
```
#### Files

```python
#Read file
file_info = flipper.storage.read("/ext/foo/bar.txt")

#Read file chunks
file_info = flipper.storage.read("/ext/foo/bar.txt", 42)

#Remove file 
flipper.storage.remove("/ext/foo/bar.txt")

#Copy file 
flipper.storage.copy("/ext/foo/source.txt", "/ext/bar/destination.txt")

#Rename file 
flipper.storage.rename("/ext/foo/bar.txt", "/ext/foo/rab.txt")

#MD5 Hash file 
flipper.storage.md5("/ext/foo/bar.txt")

#Write file in one chunk
file = "/ext/bar.txt"

text = """There are many variations of passages of Lorem Ipsum available, 
but the majority have suffered alteration in some form, by injected humour, 
or randomised words which don't look even slightly believable. 
If you are going to use a passage of Lorem Ipsum, 
you need to be sure there isn't anything embarrassing hidden in the middle of text. 
"""

flipper.storage.write.write_chunk(file, text)

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
#Set red led on
flipper.led.set('r', 255)

#Set blue led off
flipper.led.set('b', 0)

#Set green led value
flipper.led.set('g', 175)

#Set backlight on
flipper.led.set('bl', 255)

#Set backlight off
flipper.led.set('bl', 0)

#Set backlight value
flipper.led.set('bl', 175)

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
### MusicPlayer

```python
#Play song in RTTTL format
rttl_song = "Littleroot Town - Pokemon:d=4,o=5,b=100:8c5,8f5,8g5,4a5,8p,8g5,8a5,8g5,8a5,8a#5,8p,4c6,8d6,8a5,8g5,8a5,8c#6,4d6,4e6,4d6,8a5,8g5,8f5,8e5,8f5,8a5,4d6,8d5,8e5,2f5,8c6,8a#5,8a#5,8a5,2f5,8d6,8a5,8a5,8g5,2f5,8p,8f5,8d5,8f5,8e5,4e5,8f5,8g5"

flipper.music_player.play(song)

#Beep
flipper.music_player.beep()
```
### NFC

```python
#Define a callback
def on_data(data):
    print(data)

#Detect NFC
flipper.nfc.detect(callback=on_data, timeout=5)

#Emulate NFC
flipper.nfc.emulate(callback=on_data, timeout=5)

#Activate field (Default timer is 10 seconds)
flipper.nfc.field(callback=on_data)
```

## Optimizations

Feel free to contribute in any way

## Roadmap

- Implement all the cli functions


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
