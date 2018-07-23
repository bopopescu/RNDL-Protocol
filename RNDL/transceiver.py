# Transceiver class for using the RNDL protocol and normal lora messages
# created by Felix Holz, 2018-07-16

import encoder
import sys
import serial
import serialutil as ser
from threading import *
import time

# the Transceiver is a wrapper class for the RNDL protocol as well as for normal lora messages
#   to send strings with lora the strings are encoded into a hexadecimal string
#   to symbolize the end of a message the code 0x00 is appended at the end
#   the received data is decoded to a string
class Transceiver:

    def __init__(self, port):
        self.sentence = []

        # serial port properties of the lora board (RN2383)
        self.s = serial.Serial()
        self.s.port = port
        self.s.baudrate = 57600
        self.s.parity = serial.PARITY_NONE
        self.s.timeout = None
        self.s.open()

        self.init_lora()

    def __del__(self):
        self.s.close()

    # initialize the lora board (RN2383)
    def init_lora(self):
        self.s.write(b"sys get ver\r\n")
        r = self.s.read_until(terminator=b"\n")
        print(ser.clean_message(r))

        ser.write("mac pause", self.s)
        ser.read(self.s)

    # start slave mode with the given address and callback
    #   - when a message is received, it is passed on to the callback function which returns the answer
    #   - the answer is then transmittetd back to the master
    def start_slave(self, addr, callback):
        while True:
            data = self.receive()
            print("received request: " + data)

            data = data.split(";")
            if data[0] == "Q":
                print(data[1])
                print(addr)
                print(str(data[1] == addr))
                if data[1] == addr:
                    self.transmit("A;" + callback(data[2]))
        
    # request data from a slave device
    #   addr: address of the slave
    #   msg: message transmitted to the slave
    def request_data(self, addr, msg):
        self.transmit("Q;" + str(addr) + ";" + str(msg))

        reply = self.receive()
        #print(reply)
        reply = reply.split(";")
        return reply[1]
        #TODO: implement timeout

    # transmit simple string using lora
    def transmit(self, msg):
        encoded = encoder.encodehex(msg)
        encoded[-1] += "00"
        for single in encoded:
            print("sending " + single)
            ser.write("radio tx " + single, self.s)
            ser.read(self.s)
            ser.read(self.s)

    # receive simple string using lora
    def receive(self):
        while True:
            ser.write("radio rx 0", self.s)
            ser.read(self.s) #ok

            value = ser.read(self.s).decode()

            # replace control characters from the received string
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
                    #pass
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
                    self.sentence = []
                    return received