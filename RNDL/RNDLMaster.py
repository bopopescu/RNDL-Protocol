# Console application for the RNDL Master Device
# created by Felix Holz, 2018-07-17

from transceiver import Transceiver
import serialutil as ser
import encoder

trans = Transceiver("COM10")

while True:
    msg = input("message: ")
    print(trans.request_data("1", msg))
