import serial

s = serial.Serial()
s.port = "COM3"
s.baudrate = 57600
s.parity = serial.PARITY_NONE
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
print(receive(s))

write("radio set pwr 14", s)
print(receive(s))

while True:
    letter = input("letter: ")
    letter = ord(letter)
    write("radio tx " + str(letter), s)
    print(receive(s))
    print(receive(s))
    


s.close()
