import encoder
import sys
import serial
import serialutil as ser

class Transceiver:

    def __init__(self, port):
        self.sentence = []

        self.s = serial.Serial()
        self.s.port = port
        self.s.baudrate = 57600
        self.s.parity = serial.PARITY_NONE
        self.s.timeout = None
        self.s.open()

        self.init_lora()

    def __del__(self):
        self.s.close()

    def init_lora(self):
        self.s.write(b"sys get ver\r\n")
        r = self.s.read_until(terminator=b"\n")
        print(ser.clean_message(r))

        ser.write("mac pause", self.s)
        ser.read(self.s)

    def start_slave(self, addr, callback):
        while True:
            data = self.receive()
            print("received request: " + data)
            self.transmit(callback(data)) #TODO: implement FILL message
        

    def request_data(self, addr, msg):
        self.transmit("REQ." + str(msg) + ".FROM." + str(addr))
        reply = self.receive()
        print(reply)

    #transmits msg over lora
    def transmit(self, msg):
        encoded = encoder.encodehex(msg)
        encoded[-1] += "00"
        for single in encoded:
            print("sending " + single)
            ser.write("radio tx " + single, self.s)
            print(ser.read(self.s))
            print(ser.read(self.s))

    #returns a received message
    def receive(self):
        while True:
            ser.write("radio rx 0", self.s)
            ser.read(self.s) #ok

            value = ser.read(self.s).decode()

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
