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

sentence = []

while True:
    write("radio rx 0", s)
    receive(s) #ok
    
    value = receive(s).decode()
    
    
    value = value.replace("b", "")
    value = value.replace("'", "")
    value = value.replace("r", "")
    value = value.replace("n", "")
    value = value.replace("\\", "")
    
    value = value.split(" ");
    if len(value) == 3:
        valueint = int(value[2])
        value = chr(int(value[2]))
        
    else:
        value = "err"

    if value != "err":
        if valueint == 0:
            print("".join(sentence))
            sentence = []
        else:
            sentence.append(value)
        
            

    
    

s.close()


