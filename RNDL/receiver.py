import serial
import time
import encoder
from serialutil import *

class Receiver():

    def __init__(self, callback):
        self.sentence = []

        self.s = serial.Serial()
        self.s.port = "COM9"
        self.s.baudrate = 57600
        self.s.parity = serial.PARITY_NONE
        self.s.timeout = None
        self.s.open()

        self.callback = callback

        self.init_lora()
        self.receive_loop()

        

    def __del__(self):
        self.s.close()

    def init_lora(self):
        self.s.write(b"sys get ver\r\n")
        r = self.s.read_until(terminator=b"\n")
        print(clean_message(r))

        write("mac pause", self.s)
        serial_receive(self.s)


    def receive_loop(self):
        while True:
            write("radio rx 0", self.s)
            serial_receive(self.s) #ok

            value = serial_receive(self.s).decode()

            value = value.replace("b", "")
            value = value.replace("'", "")
            value = value.replace("r", "")
            value = value.replace("n", "")
            value = value.replace("\\", "")
            value = value.replace("  ", " ")

            value = value.split(" ")
            
            if len(value) == 2:

                value[1] = value[1].replace("\\r\\n", "")
                valueint = 1
                try:
                    ts = value[1]
                    valueint = 0 if ts[-4:-2] == "00" else 1
                    pass
                except ValueError:
                    pass
                
                value = encoder.decodehex(value[1])
                print("Received packet (" + str(len(value)) + ")")
                
            else:
                value = None

            if value != None:
                self.sentence.append(value)

                if valueint == 0:
                    received = "".join(self.sentence)
                    self.callback(received)
                    self.sentence = []

def cb(msg):
    print(msg)


rec = Receiver(cb)
