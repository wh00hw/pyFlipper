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

### Example

```python
from pyflipper import PyFlipper

#Instantiate flipper object with the correct serial port
flipper = PyFlipper("/dev/ttyACM0")

#Get flipper date
date = flipper.date.date()

#Get flipper timestamp
timestamp = flipper.date.timestamp()

#Get the processes dict list
ps = flipper.ps.ps()

#Get device info dict
device_info = flipper.device_info.device_info()

#Get memory info dict
memory = flipper.free.free()

#Get bluetooth info
bt_info = flipper.bt.hci_info()

#Get the storage /ext info
ext_info = flipper.storage.info('/ext')

#Get the storage /ext list
ext_list = flipper.storage.info('/ext')

#Get the storage /ext tree
ext_tree = flipper.storage.info('/ext')

#Set red led on
flipper.led.set('r', 255)

#Set vibro True or False
flipper.vibro.set(True)

#Set vibro on
flipper.vibro.on()

#Set vibro off
flipper.vibro.off()
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