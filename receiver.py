import serial
import time

s = serial.Serial()
s.port = "COM7"
s.baudrate = 57600
s.parity = serial.PARITY_NONE
s.timeout = None

s.open()


def write(msg, port):
    port.write((msg + "\r\n").encode())

def receive(port):
    value = port.read_until(terminator=b"\r\n")
    return value


#test
s.write(b"sys get ver\r\n")
r = s.read_until(terminator=b"\n")
print(r)

write("mac pause", s)
receive(s)

while True:
    write("radio rx 0", s)
    receive(s) #ok
    
    value = receive(s)
    print(value)
    

s.close()


