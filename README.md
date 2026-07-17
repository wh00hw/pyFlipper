# PyFlipper

Flipper Zero Python CLI Wrapper

![](https://thumb.tildacdn.com/tild3332-3839-4061-b663-363464303432/-/resize/214x/-/format/webp/noroot.png)

## Articles
- [How to hack a restaurant](https://medium.com/@nic_whr/how-to-hack-a-restaurant-5d394be105a9)

## Functions and characteristics:
 - [x] Flipper serial CLI wrapper
 - [x] Websocket client interface
 - [x] Plain TCP interface

## What's new (firmware 1.x compatibility)

This release brings the wrapper in line with the current Flipper Zero CLI
(validated on real hardware, firmware `unlshd-089e`):

- **New `info` module**: `flipper.info.device_info()` / `power_info()` /
  `power_debug_info()` (the modern `info device` / `info power` commands).
- **`power info` → `info power`**: `flipper.power.info()` keeps working and now
  reads `info power` under the hood. Added `flipper.power.otg_on()/otg_off()`.
- **`date`**: use `flipper.date.datetime()`; parsing was fixed for the current
  output format.
- **Storage**: sizes are parsed as both `KB` and `KiB`, `read()` now returns
  full multi-line file content, and exFAT / empty-label cards parse correctly
  (fixes #21).
- **Infrared**: the protocol list is read live from the firmware, so `NECext`,
  `Kaseikyo`, `RCA`, `Pioneer`, … are supported automatically (fixes #15). New
  `flipper.ir.protocols()`.
- **`debug` → `sysctl debug`**, **`subghz tx/rx`** gained the required
  `device` argument, **`bt hci_info`** unchanged.
- **NFC rewritten** for the current interactive sub-shell (`scan`, `dump`,
  `emulate`, `field`, `apdu`, `raw`, `mfu`) with per-UID Mifare Classic key
  cache helpers (`import_nfc_keys`, `write_key_cache`).
- **Unified serial layer** (serial / websocket / TCP) with ANSI-escape handling
  for the current shell, plus a hardware-free test suite.
- **Removed from stock firmware** (kept for custom firmwares that still ship
  them): `ps` (→ `top`), `music_player`, `nfc detect`.

## Setup instructions:

```bash
$ pip install pyflipper
```

### Tested on:
 - [x] Python 3.8.10 on Linux 5.4.0 x86_64
 - [x] Python 3.9.10 on Windows 10
 - [x] Python 3.10.5 on Android 12 (Termux + [OTGSerial2WebSocket](https://play.google.com/store/apps/details?id=com.wh00hw.serial2websocket) NO ROOT REQUIRED)
 - [x] Python 3.12 on Linux (firmware `unlshd-089e`)

## Usage/Examples

### Connection

```python
from pyflipper import PyFlipper

# Local serial port
flipper = PyFlipper(com="/dev/ttyACM0")

# OR

# Remote serial2websocket server
flipper = PyFlipper(ws="ws://192.168.1.5:1337")

# TCP
flipper = PyFlipper(tcp='192.168.89.222:22170')
```

### Power

```python
# Info (on current firmware this reads `info power` under the hood)
info = flipper.power.info()

# Poweroff
flipper.power.off()

# Reboot
flipper.power.reboot()

# Reboot in DFU mode
flipper.power.reboot2dfu()

# Toggle the 5V OTG pin on the GPIO header
flipper.power.otg_on()
flipper.power.otg_off()
```

### Update/Backup

```python
# Install update from .fuf file
flipper.update.install(fuf_file="/ext/update.fuf")

# Backup Flipper to .tar file
flipper.update.backup(dest_tar_file="/ext/backup.tar")

# Restore Flipper from backup .tar file
flipper.update.restore(bak_tar_file="/ext/backup.tar")
```

### Loader

```python
# List installed apps
apps = flipper.loader.list()

# Open app
flipper.loader.open(app_name="Clock")
```

### Flipper Info

```python
# Get flipper date (datetime object)
date = flipper.date.datetime()

# Get flipper timestamp
timestamp = flipper.date.timestamp()

# Get device info dict (current firmware `info device`, dot-separated keys)
device_info = flipper.info.device_info()

# Get power info dict (current firmware `info power`)
power_info = flipper.info.power_info()

# Extended power/gauge debug info
power_debug = flipper.info.power_debug_info()

# Legacy `device_info` command (underscore-separated keys, still supported)
legacy_info = flipper.device_info.info()

# Get heap info dict
heap = flipper.free.info()

# Get free_blocks string
free_blocks = flipper.free.blocks()

# Get bluetooth info
bt_info = flipper.bt.info()
```

> **Firmware compatibility.** This library now targets the current Flipper Zero
> CLI (firmware 1.x, verified against Unleashed `unlshd-089e`). A few legacy
> commands were removed from official firmware and are therefore **no longer
> available**: `ps` (replaced by the interactive `top`), `music_player`, and
> `nfc detect` (NFC is now an interactive sub-shell). `power info` moved to
> `info power`, `debug` moved to `sysctl debug`, and `storage` now reports sizes
> in `KiB` — all handled transparently by the wrappers above.

### Storage

#### Filesystem Info

```python
# Get the storage filesystem info
ext_info = flipper.storage.info(fs="/ext")
```

#### Explorer

```python
# Get the storage /ext dict
ext_list = flipper.storage.list(path="/ext")

# Get the storage /ext tree dict
ext_tree = flipper.storage.tree(path="/ext")

# Get file info
file_info = flipper.storage.stat(file="/ext/foo/bar.txt")

# Make directory
flipper.storage.mkdir(new_dir="/ext/foo")
```

#### Files

```python
# Read file
plain_text = flipper.storage.read(file="/ext/foo/bar.txt")

# Remove file
flipper.storage.remove(file="/ext/foo/bar.txt")

# Copy file
flipper.storage.copy(src="/ext/foo/source.txt", dest="/ext/bar/destination.txt")

# Rename file
flipper.storage.rename(file="/ext/foo/bar.txt", new_file="/ext/foo/rab.txt")

# MD5 Hash file
md5_hash = flipper.storage.md5(file="/ext/foo/bar.txt")

# Write file in one chunk
file = "/ext/bar.txt"

text = """There are many variations of passages of Lorem Ipsum available, 
but the majority have suffered alteration in some form, by injected humour, 
or randomised words which don't look even slightly believable. 
If you are going to use a passage of Lorem Ipsum, 
you need to be sure there isn't anything embarrassing hidden in the middle of text. 
"""

flipper.storage.write.file(path=file, text=text)

# Write file using a listener
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

# Don't forget to stop
flipper.storage.write.stop()
```

### LED/Backlight

```python
# Set generic led on (r,b,g,bl)
flipper.led.set(led='r', value=255)

# Set blue led off
flipper.led.blue(value=0)

# Set green led value
flipper.led.green(value=175)

# Set backlight on
flipper.led.backlight_on()

# Set backlight off
flipper.led.backlight_off()

# Turn off led
flipper.led.off()
```

### Vibro

```python
# Set vibro True or False
flipper.vibro.set(True)

# Set vibro on
flipper.vibro.on()

# Set vibro off
flipper.vibro.off()
```

### GPIO

```python
# Set gpio mode: 0 - input, 1 - output
flipper.gpio.mode(pin_name=PIN_NAME, value=1)

# Set gpio pin value: 0 - off, 1 - on
flipper.gpio.set(pin_name=PIN_NAME, value=1)

# Read gpio pin value
flipper.gpio.read(pin_name=PIN_NAME)
```

### MusicPlayer

> ⚠️ **Removed from official firmware.** The `music_player` CLI command was
> dropped from stock firmware (the app is now a separate `.fap`). These calls
> still work on custom firmwares that keep the command (e.g. Unleashed /
> RogueMaster builds that ship it); on stock firmware they return a
> "command not found" reply.

```python
# Play song in RTTTL format
rttl_song = "Littleroot Town - Pokemon:d=4,o=5,b=100:8c5,8f5,8g5,4a5,8p,8g5,8a5,8g5,8a5,8a#5,8p,4c6,8d6,8a5,8g5,8a5,8c#6,4d6,4e6,4d6,8a5,8g5,8f5,8e5,8f5,8a5,4d6,8d5,8e5,2f5,8c6,8a#5,8a#5,8a5,2f5,8d6,8a5,8a5,8g5,2f5,8p,8f5,8d5,8f5,8e5,4e5,8f5,8g5"

# Play in loop
flipper.music_player.play(rtttl_code=rttl_song)

# Stop loop
flipper.music_player.stop()

# Play for 20 seconds
flipper.music_player.play(rtttl_code=rttl_song, duration=20)

# Beep
flipper.music_player.beep()

# Beep for 5 seconds
flipper.music_player.beep(duration=5)
```

### NFC

On current firmware NFC is an interactive **sub-shell** (`scanner`, `dump`,
`emulate`, `field`, `apdu`, `raw`, `mfu`). This wrapper enters the sub-shell,
runs one command and leaves again, so each method is a normal blocking call.
`detect()` is kept as an alias of `scan()`.

```python
# Detect the tag type -> {'protocols': ['Mifare Classic'], 'raw': '...'} or None
tag = flipper.nfc.scan(timeout=5)

# Turn the NFC field on for a few seconds
flipper.nfc.field(timeout=3)

# Send an APDU (ISO14443-4 / ISO15693-3); protocol auto-detected if omitted
resp = flipper.nfc.apdu(["00A4 04 00", "A0 00"], protocol="14_4a")

# Send raw bytes with CRC appended
flipper.nfc.raw("93 20", protocol="14a", crc=True)

# Mifare Ultralight helpers
info = flipper.nfc.mfu_info()
block4 = flipper.nfc.mfu_read_block(4)
flipper.nfc.mfu_write_block(4, "00 01 02 03")

# Emulate a saved .nfc file
flipper.nfc.emulate(file="/ext/nfc/mycard.nfc", timeout=10)
```

#### Dumping a Mifare Classic over the CLI

The CLI `dump` does **not** run a dictionary attack: it reads keys from a
per-UID cache at `/ext/nfc/.cache/<UID>.keys` (the file the GUI writes after a
successful read). If that cache is missing, `dump` returns *"failed to read"*.
You can (re)create it from an existing Flipper `.nfc` dump — the keys are taken
from each sector trailer:

```python
# Load keys from a native .nfc dump into the per-UID key cache
uid, cache_path = flipper.nfc.import_nfc_keys("/path/to/card.nfc")

# Now the CLI dump can read the card (protocol tokens: mfc, mfu, 14_4a, ...)
flipper.nfc.dump(protocol="mfc", file="/ext/nfc/card_dump.nfc")
```

### RFID

```python
# Synchronous default timeout 5 seconds

# Read RFID
rfid = flipper.rfid.read()

# Emulate RFID
emulated = flipper.rfid.emulate(key_type="EM4100", key_data="5500824806")

# Write RFID
written = flipper.rfid.write(key_type="EM4100", key_data="5500824806")
```

### SubGhz

```python
# Transmit hex_key N times (default count=10, device=0 -> CC1101_INT, 1 -> CC1101_EXT)
flipper.subghz.tx(hex_key="DEADBEEF", frequency=433920000, count=5, device=0)

# Receive (default frequency=433920000 device=0 raw=False timeout=5 seconds)
received = flipper.subghz.rx(frequency=433920000, device=0, raw=True, timeout=10)

# Replay recorded transmission
flipper.subghz.tx_from_file("/ext/subghz/foo.sub")

# Decode raw .sub file
decoded = flipper.subghz.decode_raw(sub_file="/ext/subghz/foo.sub")
```

### Infrared

```python
# List the protocols supported by the connected firmware (read live from `ir` help)
protocols = flipper.ir.protocols()

# Transmit hex_address and hex_command selecting a protocol
flipper.ir.tx(protocol="Samsung32", hex_address="C000FFEE", hex_command="DEADBEEF")

# NECext is now supported (protocol list is read from the firmware, not hardcoded)
flipper.ir.tx(protocol="NECext", hex_address="EF00", hex_command="FD02")

# Raw Transmit samples
flipper.ir.tx_raw(frequency=38000, duty_cycle=0.33, samples=[1337, 8888, 3000, 5555])

# Synchronous default timeout 5 seconds
# Receive tx
r = flipper.ir.rx(timeout=10)
```

### IKEY

```python
# Read (default timeout 5 seconds)
ikey = flipper.ikey.read()

# Write (default timeout 5 seconds)
flipper.ikey.write(key_type="Dallas", key_data="DEADBEEFCOOOFFEE")

# Emulate (default timeout 5 seconds)
flipper.ikey.emulate(key_type="Dallas", key_data="DEADBEEFCOOOFFEE")
```

### Log

```python
# Attach event logger (default timeout 10 seconds)
logs = flipper.log.attach()
```

### Debug

```python
# Activate debug mode (issues `sysctl debug 1` on current firmware)
flipper.debug.on()

# Deactivate debug mode
flipper.debug.off()
```

### Onewire

```python
# Search
response = flipper.onewire.search()
```

### I2C

```python
# Get
response = flipper.i2c.get()
```

### Input

```python
# Input dump
dump = flipper.input.dump()

# Send input
flipper.input.send("up", "press")
```

## Tests

The suite is split in two:

- **Hardware-free tests** (`test_serial_wrapper.py`, `test_commands.py`) run
  anywhere — they drive the library against a simulated serial port
  (`tests/fake_serial.py`) that reproduces the Flipper CLI framing, so no device
  is required. These run in CI.
- **Hardware integration tests** (`test_hardware.py`) talk to a real Flipper and
  are **skipped automatically** when no device is connected. Set
  `FLIPPER_COM=/dev/ttyACM0` to pin a specific port.

```bash
# Everything (hardware tests self-skip if no Flipper is attached)
python -m unittest discover -s tests -p "test_*.py" -v

# Only the hardware-free tests
python -m unittest tests.test_serial_wrapper tests.test_commands -v
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
