import sys
import serial
import encoder
from serialutil import *

 #transmit single message over LoRa
    def transmit(s, msg):
        encoded = encoder.encodehex(msg)
        encoded[-1] += "00"
        for single in encoded:
            write("radio tx " + single, s)
            print("sending " + single)
            serial_receive(s)
            serial_receive(s)

    #returns single message received over LoRa
    def receive(s):
        sentence = []
        while True:
            write("radio rx 0", s)
            serial_receive(s) #ok

            value = serial_receive(s).decode()

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
                sentence.append(value)

                if valueint == 0:
                    received = "".join(sentence)
                    return received
                    sentence = []