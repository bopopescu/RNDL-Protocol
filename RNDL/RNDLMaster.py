from transceiver import Transceiver
import serialutil as ser
import encoder

trans = Transceiver("COM3")

while True:
    msg = input("peta: ")
    trans.request_data("12", msg)
