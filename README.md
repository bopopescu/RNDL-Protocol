# RNDL-Protocol
Simple request-based protocol used for transferring IoT data over LoRa.

## Command structure
All transmitted messages use the ASCII character set. Every message can be recieved by every device, but only the device with the corresponding address.

### Request
The Request message has the following structure:
> Q;**address**;**message**

### Response
The Response message has the following structure:
> A;**message**

## Usage
Every device on the network has to be either a Master or a Slave. The Master requests data and the Slaves respond to the requests. Every network should only have one master. The number of slaves is not limited.

### Master
A working implementation of the Master Device can be found in the RNDLMasterGUI.py script. It is a simple GUI application with inputs for address and message.
In order to make your own implementation the Transceiver class can be used. It has many functions to transmit and receive a normal message using LoRa, and it also implements the RNDL protocol. 
#### Simple Request

```python
from transceiver import Transceiver

trans = Transceiver("COM9")
print(trans.request_data("1", "temperature"))

```

### Slave
The Slave Device is implemented in RNDLSlave.py, which asks for a reply in the console when receiving a message. 

#### Arduino implementation
The RNDL Protocol is also implemented in C++ for use with an Arduino. An example implementation can be found in Arduino/app.ino.
##### #define preprocessor directives
To make the Arduino code more versatile, macros were used.

#define | effect
--- | ---
DEBUG | Enable debug statements on the default serial interface
KEYBOARD | Enable keyboard input with an Arduino Uno as Serial Passthrough
UNO_SOFTWARE_SERIAL | Enables second Software Serial. Required for the keyboard.
DHT_CONNECTED | Enables a DHT Sensor

#### Simple Slave Device

```python
from transceiver import Transceiver

def callback(msg):
  if msg == "Hello World":
    return "Hello!"
  else:
    return "Unknown command"

trans = Transceiver("COM1")
trans.start_slave("2", callback)

```

## Encoding
All messages are encoded in order to optimize the transmission speed. The encoding works as follows:
- every message is split into packets with the size n
- every character of the package is converted into a hexadecimal string
- all hexadecimal strings of a packet are joined together into a single string
- at the end of the last packet, the values "00" are added to symbolize the end of a message
- each packet is transmitted seperately

### Example
To encode the message "Hello World!" with a packet size of 4 the following steps are taken:
- "Hello World!" -> "Hell", "o Wo", "rld!"
- "Hell", "o Wo", "rld!" -> "48656C6C", "6F20576F", "726C6421"
- "48656C6C", "6F20576F", "726C6421" -> "48656C6C", "6F20576F", "726C642100"
- transmit every packet over LoRa
