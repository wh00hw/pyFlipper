from pyflipper import PyFlipper

#Instantiate flipper object with the correct serial port
flipper = PyFlipper("/dev/ttyACM0")

#Get flipper date
date = flipper.date.date()

#Get flipper timestamp
timestamp = flipper.date.timestamp()

#Get the processes dict list
processes = flipper.ps.ps()

#Get device info dict
device_info = flipper.device_info.device_info()

#Get memory info dict
memory = flipper.free.free()

#Get bluetooth info
bt_info = flipper.bt.hci_info()

#Get the storage /ext info
storage_info = flipper.storage.info('/ext')

#Get the storage /ext list
ext_dir = flipper.storage.info('/ext')

#Get the storage /ext tree
ext_tree = flipper.storage.info('/ext')

#Set red led on
flipper.led.set('r', 255)

#Set vibro on
flipper.vibro.on()

#Set vibro off
flipper.vibro.off()
