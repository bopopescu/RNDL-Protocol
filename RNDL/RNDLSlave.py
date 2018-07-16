from transceiver import Transceiver
import serialutil as ser
import encoder

trans = Transceiver("COM7")

while True:
    print(trans.receive())