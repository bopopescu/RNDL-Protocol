import sys
import serial
import encoder
from serialutil import *
import transceiver as tr

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

        #write("radio set pwr 14", self.s)
        #serial_receive(self.s)

    #starts an unicast request to the given address and returns the result
    def request(self, msg, addr):
        print("tr transmit static")
        tr.transmit(self.s, "REQ.test.FROM.12")
        #tr.transmit(self.s, "REQ." + msg + ".FROM." + addr)

        reply = tr.receive(self.s)
        return reply

    #starts subordinate mode. addr is the address of the device. request_callback should return an answer based on the request parameter
    def start_subordinate(self, addr, request_callback):
        while True:
            req = tr.receive(self.s)
            print(req)

            req = req.split(".")

            print("===================")
            
            req[-1] = req[-1][:-1]

            print(req)
            r = req[1]
            a = req[3]

            if a == addr:
                response = request_callback(r)
                print(response)
                tr.transmit(self.s, response)
        

   
