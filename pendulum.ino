#define LED 13

#define IPIN0 2 // CHANNEL B
#define IPIN1 3 // CHANNEL A

volatile int angle;  // What is the current angle?

volatile int state0 = LOW;  // what is the state of pin 0?
volatile int state1 = LOW;  // what is the state of pin 1?

long int t0;

int going=0;

void blink0() {    
    state0 = digitalRead(IPIN0);  // state0 has changed. check state0 and state1 and update angle.
    state1 = digitalRead(IPIN1);

    digitalWrite(LED,state0);     // let the LED know we're here.

    if (state0) {
      if (state1) {
        angle -= 1;
      } else {
        angle += 1;
      }
    } else {
      if (state1) {
        angle += 1;
      } else {
        angle -= 1;
      }
    }
}

void blink1() {
    state0 = digitalRead(IPIN0);   // state1 has changed. check state0 and state1 and update angle.
    state1 = digitalRead(IPIN1);
    if (state0) {
      if (state1) {
        angle += 1;
      } else {
        angle -= 1;
      }
    } else {
      if (state1) {
         angle -= 1;
      } else {
        angle += 1;
      }
    }
}

void setup() {
    pinMode(LED, OUTPUT);
    Serial.begin(9600);
    attachInterrupt(digitalPinToInterrupt(IPIN0), blink0, CHANGE);
    attachInterrupt(digitalPinToInterrupt(IPIN1), blink1, CHANGE);
    Serial.println("Ready");  // tell the computer we're ready
    Serial.println("Time,Angle");
}

void loop() {
  char command;
  if (Serial.available()>0) {          // are there characters to read?
    command = (char)Serial.read();     // grab one
    if (command=='g') {                // check it
      going=1;
      angle=0;
      t0=millis();
    } else if (command=='s') {
      going=0;
    }
  }
  if (going) {  
    Serial.print(1.0*(millis()-t0)/1000,3);
    Serial.print(",");
    Serial.println(360.0*angle/2048,3);
  }
}


