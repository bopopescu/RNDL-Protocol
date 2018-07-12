import serial
import encoder
from serialutil import *

s = serial.Serial()
s.port = "COM8"
s.baudrate = 57600
s.parity = serial.PARITY_NONE
s.open()

#test
s.write(b"sys get ver\r\n")
r = s.read_until(terminator=b"\n")
print(clean_message(r))

write("mac pause", s)
receive(s)

write("radio set pwr 14", s)
receive(s)

while True:
    sentence = input("sentence: ")
    encoded = encoder.encodehex(sentence)
    encoded[-1] += "00"
    for single in encoded:
        write("radio tx " + single, s)
        print("sending " + single)
        receive(s)
        receive(s)

s.close()
