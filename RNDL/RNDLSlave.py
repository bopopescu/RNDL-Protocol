# Console application for the RNDL Slave device
# created by Felix Holz, 2018-07-17

from transceiver import Transceiver
import serialutil as ser
import encoder

def callback(msg):
    return input("reply: ")

trans = Transceiver("COM8")

trans.start_slave("2", callback)
