import serial
import encoder
from serialutil import write
from serialutil import receive

s = serial.Serial()
s.port = "COM3"
s.baudrate = 57600
s.parity = serial.PARITY_NONE
s.open()

#test
s.write(b"sys get ver\r\n")
r = s.read_until(terminator=b"\n")
print(r)

write("mac pause", s)
receive(s)

write("radio set pwr 14", s)
receive(s)

while True:
    sentence = input("sentence: ")
    encoded = encoder.encodehex(sentence)
    for single in encoded:
        write("radio tx " + single, s)
        print("sending " + single)
        print(receive(s))
        print(receive(s))

    write("radio tx 0", s)
    receive(s)
    receive(s)
        
s.close()
