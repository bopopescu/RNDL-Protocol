import serial

s = serial.Serial()
s.port = "COM3"
s.baudrate = 57600
s.parity = serial.PARITY_NONE
s.open()

s.write(b"sys get ver\r\n")

r = s.read_until(terminator=b"\n")

print(r)



s.close()
