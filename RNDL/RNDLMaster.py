from transceiver import Transceiver
import serialutil as ser
import encoder

trans = Transceiver("COM10")

while True:
    msg = input("peta: ")
    print(trans.request_data("1", msg))
