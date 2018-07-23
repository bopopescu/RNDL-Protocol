# write data to a serial port using the termination characters of the lora board (RN2383)
def write(msg, port):
    port.write((msg + "\r\n").encode())

# read data from a serial port using the termination characters of the lora board (RN2383)
def read(port):
    value = port.read_until(terminator=b"\r\n")
    return value

# remove control characters from a message
def clean_message(msg):
    msg = msg.decode()    
    msg = msg.replace("b", "")
    msg = msg.replace("'", "")
    msg = msg.replace("r", "")
    msg = msg.replace("n", "")
    msg = msg.replace("\\", "")
    msg = msg.replace("  ", " ")
    return msg
