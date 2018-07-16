import sys
import serial
import encoder
from serialutil import *

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class RNDLDevice():

    def __init__(self, port):
        self.sentence = []
        self.s = serial.Serial()
        self.s.port = port
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
        serial_receive(self.s)

        write("radio set pwr 14", self.s)
        serial_receive(self.s)

    #starts an unicast request to the given address and returns the result
    def request(self, msg, addr):
        transmit("REQ." + msg + ".FROM." + addr)
        reply = serial_receive()

    #starts slave mode. addr is the address of the device. request_callback should return an answer based on the request parameter
    def start_slave(self, addr, request_callback):
        while True:
            req = self.receive()
            req = req.split(".")
            req[-1] = req[-1][:-1]
            r = req[1]
            a = req[3]

            if int(a) == addr:
                response = request_callback(r)
                self.transmit(response)
        

    #transmit single message over LoRa
    def transmit(self, msg):
        encoded = encoder.encodehex(msg)
        encoded[-1] += "00"
        for single in encoded:
            write("radio tx " + single, self.s)
            print("sending " + single)
            serial_receive(self.s)
            serial_receive(self.s)

    #returns single message received over LoRa
    def receive(self):
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
                    return received
                    self.sentence = []


def cb(r):
    return "answer"


device = RNDLDevice()
device.start_slave(12, cb)

input("tt")


