from RNDLDevice import *

device = RNDLDevice("COM3")

while True:
    msg = input("message: ")
    device.request("12", msg)
