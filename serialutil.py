
def write(msg, port):
    port.write((msg + "\r\n").encode())

def receive(port):
    value = port.read_until(terminator=b"\r\n")
    return value

def clean_message(msg):

    msg = msg.decode()
    
    msg = msg.replace("b", "")
    msg = msg.replace("'", "")
    msg = msg.replace("r", "")
    msg = msg.replace("n", "")
    msg = msg.replace("\\", "")
    msg = msg.replace("  ", " ")

    return msg
