import math

LORA_MAX_DIGITS = 480
LORA_MAX_CHARS = 160

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

   
    
        


    

string = "asfhjsdkfhljksdhfjkhsdajkfhsdjakhfjkadshfsadhfsdhfjsadlfjsdahflsdajfhsdajfhsdajlfadslkfhlsadjkfsadlfsllllllaskjfhasdjkfhlljksadhfjlksadhfjksdahfjksdahfkjsdahfjksdahfjksadhfkjasdhfkjasdlhfkjlsaldhfjklsadlhfjklsadhfjkasdhfjksadhfjksadhfjksadhfjklsadlhfkjasdhfjksadhfjkadshfjkasdhfjksadhfkjasdhfkjasdljfs"
print(len(string))
value = encode_packet(string)
print(value)



