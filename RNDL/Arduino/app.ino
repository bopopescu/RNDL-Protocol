#include <DHT_U.h>
#include <DHT.h>

// Arduino sketch which implements the RNDL protocol and simple lora messaging
// created by Felix Holz, 2018-07-18
#include <LiquidCrystal.h>
#include <PS2Keyboard.h>
#include <SoftwareSerial.h>

//#define DEBUG
#define DHT_CONNECTED
// print data to serial port for debugging
#ifdef DEBUG
    #define PRINT(x) Serial.println(x)
#else
    #define PRINT(x) 
#endif

#ifdef DHT_CONNECTED
    DHT dht(14, DHT22);
#endif
// connection used to communicate with the lora board (RN2383)
SoftwareSerial lora(5, 4); // RX, TX
SoftwareSerial uno(13, 15); // RX, TX



// maximum characters transmitted in a single packet
const int MAX_HEX_CHARS = 10;

//PS2Keyboard keyboard;
//String keyboardbuffer = "";

//const int rs = 13, en = 12, d4 = 8, d5 = 9, d6 = 10, d7 = 11;
//LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


// read a reply from the lora board (RN2383) over the serial interface
String read_serial()
{
    while(lora.available() == 0)
    {
        ESP.wdtFeed();
    }

    return lora.readStringUntil('\n');
}

// write a command to the lora board (RN2383) over serial using the correct termination characters (CR+LF)
void write_serial(String msg)
{
    lora.print(msg + "\r\n");
}

// sets up the lora board (RN2383)
void setup_lora()
{
    write_serial("sys get ver");
    read_serial();
    
    write_serial("mac pause");
    read_serial();
}

// sends a single message using lora and the RNDL protocol
void send_lora(String msg)
{
    int msglen = msg.length();

    int it = 1 + ((msglen - 1) / MAX_HEX_CHARS);
    String encoded[it];
    String splitmsg[it];
    for(int i = 0; i < it; i++)
    {
        splitmsg[i] = msg.substring(i*MAX_HEX_CHARS, i*MAX_HEX_CHARS + MAX_HEX_CHARS);
    }

    for(int i = 0; i < it; i++)
    {
        encoded[i] = String();
        for(int j = 0; j < splitmsg[i].length(); j++)
        {
            encoded[i] += String(splitmsg[i][j], HEX);
        }
    }
    encoded[it-1] += "00";

    for(String s : encoded)
    {
        write_serial("radio tx " + s);
        read_serial();
        read_serial();
    }
}


// read a single message using lora and the RNDL protocol
String single_read_lora()
{
    bool end_of_message = false;
    String whole_message = "";

    // reads until the end off message byte (0x00) is detected
    while(!end_of_message)
    {   
        write_serial("radio rx 0");
        read_serial(); //ok
        String msg = read_serial();

        PRINT(msg);
        
        
        const int MAXBYTES = 4;
        int msglen = msg.length();

        int it = 1 + ((msglen - 1) / MAXBYTES);
        
        String splitmsg[it];

        char decoded[msglen/2];
        unsigned int deccount = 0;

        int lastspace = msg.lastIndexOf(' ');
        String tmp = msg.substring(lastspace+1);
        if(tmp.charAt(0) == 'r')
        {
            continue;
        }

        tmp.trim();
        if(tmp.endsWith("00"))
        {
            end_of_message = true;
        }

        for(int i = 0; i < it; i++)
        {
            splitmsg[i] = tmp.substring(i*MAXBYTES, i*MAXBYTES + MAXBYTES);
        }

        PRINT("==============");

        // C magic to convert a hexadecimal string to an ascii string
        for(String s : splitmsg)
        {
                PRINT(s);
                unsigned long number = strtoul(&s[0], NULL, 16);
                char c1 = number & 0xFF;
                number >>= 8;
                char c2 = number & 0xFF;
                number >>= 8;
                
                decoded[deccount] = c2;
                deccount++;
                decoded[deccount] = c1;
                deccount++;
        }

        String decodedstring(decoded);

        whole_message += decodedstring.substring(0, msglen/2+1);
        PRINT("whole_message: " + whole_message);
    }

    return whole_message;

}

// starts the slave mode of the RNDL protocol:
//      - listen to requests
//      - check if the requested address matches the device address
//      - read the message string and send the corresponding data
//      - repeat
void start_rndl_slave(String address)
{
    while(true)
    {
        String msg = single_read_lora();
        PRINT("Received request: " + msg);
        if(msg.startsWith("Q;"))
        {
            // Request String: "Q:<address>;<message>"
            // extracts the address and message from the request string
            String t1 = msg.substring(2);
            int index1 = t1.indexOf(';');
            String t_addr = t1.substring(0, index1);
            
            int index2 = t1.indexOf(';', index1);
            String req_msg = t1.substring(index2+1);

            PRINT("REQ_MSG:");
            PRINT(req_msg);
            
            // Compare addresses and send requested data
            if(address.equalsIgnoreCase(t_addr))
            {
                // read until buffer is empty
                while(uno.available())
                {
                    uno.read();
                    ESP.wdtFeed();
                }

                if(req_msg == "time")
                {
                    send_lora("A;time: " + String(millis()));
                }
                /*
                else if(req_msg == "keyboard")
                {
                    digitalWrite(LED_BUILTIN, LOW);
                    String keyboardinput = " ";
                    bool init = false;
                    while(true)
                    {
                        while(!uno.available())
                        {
                            ESP.wdtFeed();
                        }
                        char key = uno.read();
                        if(key == '\n') break;
                        keyboardinput += key;
                        ESP.wdtFeed();
                    }
                    digitalWrite(LED_BUILTIN, HIGH);
                    send_lora("A;" + keyboardinput.substring(1));
                }
                */
                else if(req_msg == "temperature")
                {
#ifdef DHT_CONNECTED
                    float temperature = dht.readTemperature();
                    if(isnan(temperature))
                    {
                        send_lora("A;MEASUREMENT_ERROR");
                    }
                    else
                    {
                        send_lora("A;" + String(temperature));
                    }
#else
                    send_lora("A;NO_SENSOR");
#endif          
                }
                else if(req_msg == "humidity")
                {
#ifdef DHT_CONNECTED
                    float humidity = dht.readHumidity();
                    if(isnan(humidity))
                    {
                        send_lora("A;MEASUREMENT_ERROR");
                    }
                    else
                    {
                        send_lora("A;" + String(humidity));
                    }
#else
                    send_lora("A;NO_SENSOR");
#endif
                }
                else
                {
                    send_lora("A;UNKNOWN_MESSAGE");
                }
            }
        }
    }
}

void setup()
{
    //keyboard.begin(2, 3, PS2Keymap_US);

    // serial communication with PC for debugging
    Serial.begin(115200);
    Serial.println("Arduino LoRa");

    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
    digitalWrite(LED_BUILTIN, HIGH);

    // serial communication with the lora board (RN2383)
    lora.begin(57600);
    uno.begin(9600);

#ifdef DHT_CONNECTED
    dht.begin();
#endif

    while(uno.available())
    {
        uno.read();
        ESP.wdtFeed();
    }
    
    // setup lora and start slave mode with given address
    setup_lora();
    start_rndl_slave("5");
}

void loop() { }