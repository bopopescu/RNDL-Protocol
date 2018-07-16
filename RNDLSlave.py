from RNDLDevice import *

device = RNDLDevice("COM9")

def cb(msg : str):
    return "reply"

device.start_slave("13", cb)

