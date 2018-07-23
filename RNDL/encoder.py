# utility functions for encoding and decoding messages
# created by Felix Holz, 2018-07-11

import math

# maximum number of characters per packet
MAX_HEX_CHARS = 10

# encode a string to the hexadecimal string used by the protocol
#   msg:    string to encode
#   return: string array of hexadecimal strings. each string has a max length of MAX_HEX_CHARS
def encodehex(msg):
    values = []
    if len(msg) > MAX_HEX_CHARS:
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

# decode a hexadecimal string to a string
#   msg:    single hexadecimal string to decode
#   return: decoded string
def decodehex(msg):
    ba = []
    for i in range(math.ceil(len(msg)/2)-1):
        s = int(msg[i*2:i*2+2], 16)
        ba.append(chr(s))
    return "".join(ba)        
    
