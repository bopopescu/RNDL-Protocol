# Console application for the RNDL Subordinate device
# created by Felix Holz, 2018-07-17

from transceiver import Transceiver
import serialutil as ser
import encoder

def callback(msg):
    return input("reply: ")

trans = Transceiver("COM9")

trans.start_subordinate("2", callback)
