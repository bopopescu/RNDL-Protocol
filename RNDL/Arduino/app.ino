
#include <LiquidCrystal.h>

#include <PS2Keyboard.h>

const int DataPin = 9;
const int IRQpin =  8;
const int MAX_HEX_CHARS = 4;

PS2Keyboard keyboard;


//const int rs = 13, en = 12, d4 = 8, d5 = 9, d6 = 10, d7 = 11;
//LiquidCrystal lcd(rs, en, d4, d5, d6, d7);



void encodehex(String msg)
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
}

void decodehex(String msg)
{
    const int MAXBYTES = 6;
    int msglen = msg.length();

    int it = 1 + ((msglen - 1) / MAXBYTES);
    
    String splitmsg[it];

    char decoded[msglen/2];
    unsigned int deccount = 0;

    for(int i = 0; i < it; i++)
    {
        splitmsg[i] = msg.substring(i*MAXBYTES, i*MAXBYTES + MAXBYTES);
    }



    for(String s : splitmsg)
    {
            unsigned long number = strtoul(&s[0], NULL, 16);
            char c1 = number & 0xFF;
            number >>= 8;
            char c2 = number & 0xFF;
            number >>= 8;
            char c3 = number & 0xFF;
            number >>= 8;

            decoded[deccount] = c3;
            deccount++;
            decoded[deccount] = c2;
            deccount++;
            decoded[deccount] = c1;
            deccount++;
    }

    String decodedstring(decoded);

    Serial.println(decodedstring.substring(0, msglen/2));





}

String keyboardstring = "";

void setup()
{



    //pinMode(7, OUTPUT);
    //digitalWrite(7, HIGH);
    keyboard.begin(2, 3, PS2Keymap_US);

    Serial.begin(115200);
    Serial.println("International Keyboard Test:");
    //encodehex("testtestt");
    decodehex("676173676173696923235544");

/*
    lcd.begin(16, 2);
    
    lcd.setCursor(0, 1);
    lcd.print("test test test");
    lcd.setCursor(0, 0);

    lcd.display();
    lcd.autoscroll();
    */
}

void loop() {
    if (keyboard.available()) 
    {
        char c = keyboard.read();
        Serial.println(c);
    }
  
  
}
