
#include <LiquidCrystal.h>
#include <PS2Keyboard.h>
#include <SoftwareSerial.h>

#define DEBUG

#ifdef DEBUG
    #define PRINT(x) Serial.println(x)
#else
    #define PRINT(x) 
#endif


SoftwareSerial lora(5, 4); // RX, TX    

const int DataPin = 9;
const int IRQpin =  8;
const int MAX_HEX_CHARS = 4;

//PS2Keyboard keyboard;

String keyboardbuffer = "";

//const int rs = 13, en = 12, d4 = 8, d5 = 9, d6 = 10, d7 = 11;
//LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


String read_serial()
{
    while(lora.available() == 0)
    {
        ESP.wdtFeed();
    }

    return lora.readStringUntil('\n');
}

void write_serial(String msg)
{
    lora.print(msg + "\r\n");
}

void setup_lora()
{
    write_serial("sys get ver");
    read_serial();
    
    write_serial("mac pause");
    read_serial();
}


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

String single_read_lora()
{

    bool end_of_message = false;

    String whole_message = "";

    int gas = 0;

    while(!end_of_message)
    {
        PRINT(gas);
        gas++;
        
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

        PRINT("ISDN");
        PRINT(tmp);
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

        for(String s : splitmsg)
        {
                PRINT(s);
                unsigned long number = strtoul(&s[0], NULL, 16);
                char c1 = number & 0xFF;
                number >>= 8;
                char c2 = number & 0xFF;
                number >>= 8;
                //char c3 = number & 0xFF;
                //number >>= 8;

                //decoded[deccount] = c3;
                //deccount++;
                decoded[deccount] = c2;
                deccount++;
                decoded[deccount] = c1;
                deccount++;
        }

        String decodedstring(decoded);

        whole_message += decodedstring.substring(0, msglen/2+1);
        PRINT("LEX: " + whole_message);
    }

    return whole_message;

}

void start_rndl_slave(String address)
{
    while(true)
    {
        String msg = single_read_lora();
        PRINT("Received request: " + msg);
        if(msg.startsWith("Q;"))
        {
            String t1 = msg.substring(2);
            int index1 = t1.indexOf(';');
            String t_addr = t1.substring(0, index1);
            
            int index2 = t1.indexOf(';', index1+1);
            Serial.println("Index2: " + index2);
            String req_msg = t1.substring(index2);

            Serial.println("MESSAGE:");

            if(address.equalsIgnoreCase(t_addr))
            {
                //TODO: check message
                int in = digitalRead(12);
                send_lora("A;D0: " + in);
            }

        }

        
    }
}

void setup()
{
    //pinMode(7, OUTPUT);
    //digitalWrite(7, HIGH);
    //keyboard.begin(2, 3, PS2Keymap_US);

    pinMode(14, INPUT);


    Serial.begin(57600);
    Serial.println("Arduino LoRa");

    lora.begin(57600);

    setup_lora();

    start_rndl_slave("1");

    //send_lora("digits hex numbers with any prefix");

}

void loop() {

    
}
