import math

MAX_HEX_CHARS = 2

def encodehex(msg):
    values = []
    if len(msg) > MAX_HEX_CHARS:
        it = len(msg) / MAX_HEX_CHARS
        it = math.ceil(it)
        for i in range(it):
            if i*(MAX_HEX_CHARS) > len(msg):
                values.append(msg[i*MAX_HEX_CHARS:(i*(MAX_HEX_CHARS))])
            else:
                values.append(msg[i*MAX_HEX_CHARS:])
    else:
        values = [ msg ]

    print(values)

    strings = []
    
    for message in values:
        temp = []
        for s in message:
            h = bytes(s, "ascii").hex()
            temp.append(h)

        temp = "".join(temp)
        strings.append(temp)
    return strings

encodehex("testt")

def decodehex(msg):
    ba = []
    for i in range(math.ceil(len(msg)/2)-1):
        print(msg[i*2:i*2+2])
        s = int(msg[i*2:i*2+2], 16)
        ba.append(chr(s))
    return "".join(ba)        
    
