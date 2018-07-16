from RNDLDevice import *

device = RNDLDevice("COM8")

while True:
    msg = input("message: ")
    device.request("12", msg)
