import math

MAX_HEX_CHARS = 20

def encodehex(msg):
    values = []
    if len(msg) > MAX_HEX_CHARS:
        #values = [msg[i:i+MAX_HEX_CHARS] for i in range(0, len(msg), MAX_HEX_CHARS)]
        for i in range(0, len(msg), MAX_HEX_CHARS):
            values.append(msg[i:i+MAX_HEX_CHARS])
        
    else:
        values = [ msg ]

    strings = []
    
    for message in values:
        temp = []
        for s in message:
            h = bytes(s, "ascii").hex()
            temp.append(h)

        temp = "".join(temp)
        strings.append(temp)
    return strings

def decodehex(msg):
    ba = []
    for i in range(math.ceil(len(msg)/2)-1):
        s = int(msg[i*2:i*2+2], 16)
        ba.append(chr(s))
    return "".join(ba)        
    
