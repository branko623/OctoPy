#include <OctoWS2811.h>

// Configure below
// Octo WS2811 utilizes the same amount of memory for each strand
// so the individual lengths if varied are not important
// Configure strip lengths in Python
#define MAX_LEDS_PER_STRIP 34

// Although the name includes "Octo", the teensy 4 iteration allows for more than 8 channels
// The DMA code allows up to 16
#define NUM_PINS 9

// pin list in order. Teensy 4+ only. 
// Configure strip lengths in Python
byte pinList[NUM_PINS] = {16,11,12,14,9,7,3,5,1};
int config  = WS2811_GRB | WS2813_800kHz;


DMAMEM int displayMemory[MAX_LEDS_PER_STRIP  * NUM_PINS * 3 / 4];
int drawingMemory[MAX_LEDS_PER_STRIP  * NUM_PINS  * 3 / 4];
OctoWS2811 octo(MAX_LEDS_PER_STRIP, displayMemory, drawingMemory, config, NUM_PINS, pinList);

//int t1 = micros();
//int t2 = micros();
uint16_t pixels;

// Data Frame, get data from Serial port
void getData(){

    //t1 = micros();
    uint16_t s,i;

    for (s=0;s<MAX_LEDS_PER_STRIP*NUM_PINS; s+=MAX_LEDS_PER_STRIP)
    {
        // The first two bytes in the "Strip dataframe" signifiy how many bytes are coming in
        pixels = (Serial.read() << 8) + Serial.read();
        
        for (i=0;i<pixels;i++){
            octo.setPixel(s+i,Serial.read(),Serial.read(),Serial.read());
        }
    }

    // send back 'x' to the host saying that we are ready to recieve more data
    // sending this before show() allows the host plenty of time to figure out what to send.
    // with the teensy's DMA, we recieve data before we get here again
    Serial.print('x');
    //t2 = micros();

    octo.show(); 
    // the code to fetch from Serial and process it takes about 120 microseconds
    // show() on a max strand of 34 is about 1200 microseconds

    //Serial.print(t2-t1);
}

void setup() {
    Serial.begin(1); // value not important
    octo.begin();
}

void loop(){
    // loop until one of the following data frames are recieved
    if (Serial.available()){
        uint8_t g = Serial.read(); 

        if (g== 'D' && 
                Serial.read() == 'A' && 
                Serial.read() == 'T' &&
                Serial.read() == 'A') {
            getData();
        }
        else {
           Serial.flush();
        }
    }
}
