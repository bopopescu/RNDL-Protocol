from RNDLDevice import *

device = RNDLDevice("COM9")

def cb(msg):
    return "reply"

device.start_slave("12", cb)

