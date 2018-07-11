import math

LORA_MAX_DIGITS = 480
LORA_MAX_CHARS = 160

MAX_HEX_CHARS = 10

def encode4(msg):
    ret = 0;
    for i in range(len(msg)):
        char = msg[i]
        char = ord(char)
        ret |= char
        if i != len(msg)-1:
            ret <<= 8

    return ret

def encode_packet(msg):
    values = []
    if len(msg) > LORA_MAX_CHARS:
        it = len(msg) / LORA_MAX_CHARS
        it = math.ceil(it)
        for i in range(it):
            if i*(LORA_MAX_CHARS + 1) > len(msg):
                values.append(msg[i*LORA_MAX_CHARS:(i*(LORA_MAX_CHARS+1))])
            else:
                values.append(msg[i*LORA_MAX_CHARS:])
    else:
        values.append(msg)
             

    
    temp = ""
    iterations = len(msg) / 4
    print(iterations)
    for i in range(int(iterations)):
        enc = encode4(msg[i*4:(i*4)+4])
        temp += str(enc);

def encodehex(msg):
    values = []
    if len(msg) < MAX_HEX_CHARS:
        it = len(msg) / MAX_HEX_CHARS
        it = math.ceil(it)
        for i in range(it):
            if i*(LORA_MAX_CHARS + 1) > len(msg):
                values.append(msg[i*MAX_HEX_CHARS:(i*(MAX_HEX_CHARS+1))])
            else:
                values.append(msg[i*MAX_HEX_CHARS:])
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
    for i in range(math.ceil(len(msg)/2)):
        s = int(msg[i*2:i*2+2], 16)
        ba.append(chr(s))
    return "".join(ba)        
    

def bintohex(msg):
    d = [55, 33, 66, 244, 234, 234, 123, 12, 123]
    print(bytes(d).hex())
    
        


print(encodehex("test"))

print(decodehex(encodehex("test")[0]))

#bintohex("")

    
'''
string = "asfhjsdkfhljksdhfjkhsdajkfhsdjakhfjkadshfsadhfsdhfjsadlfjsdahflsdajfhsdajfhsdajlfadslkfhlsadjkfsadlfsllllllaskjfhasdjkfhlljksadhfjlksadhfjksdahfjksdahfkjsdahfjksdahfjksadhfkjasdhfkjasdlhfkjlsaldhfjklsadlhfjklsadhfjkasdhfjksadhfjksadhfjksadhfjklsadlhfkjasdhfjksadhfjkadshfjkasdhfjksadhfkjasdhfkjasdljfs"
print(len(string))
value = encode_packet(string)
print(value)
'''



