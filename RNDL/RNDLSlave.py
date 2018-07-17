from transceiver import Transceiver
import serialutil as ser
import encoder



def callback(msg):
    return input("reply: ")


trans = Transceiver("COM8")

trans.start_slave("12", callback)
