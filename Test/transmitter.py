import serial
import encoder
from serialutil import *



class Transmitter():

    def __init__(self):
        self.s = serial.Serial()
        self.s.port = "COM8"
        self.s.baudrate = 57600
        self.s.parity = serial.PARITY_NONE
        self.s.open()

    def __del__(self):
        self.s.close()

    def init_lora(self):
        self.s.write(b"sys get ver\r\n")
        r = self.s.read_until(terminator=b"\n")
        print(clean_message(r))
        
        write("mac pause", self.s)
        receive(self.s)

        write("radio set pwr 14", self.s)
        receive(self.s)

    def transmit(self, msg):
        encoded = encoder.encodehex(msg)
        encoded[-1] += "00"
        for single in encoded:
            write("radio tx " + single, self.s)
            print("sending " + single)
            receive(self.s)
            receive(self.s)


t = Transmitter()
t.transmit("findenig")