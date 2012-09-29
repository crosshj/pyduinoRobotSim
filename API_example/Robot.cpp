#include "Robot.h"

#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "string.h"

extern HardwareSerial Serial;


Robot::Robot(void){
  // maybe should set up pins for comm with other Arduinos here
    
    Wire.begin();
        
    for (int i=0; i < 16; i++)
    {
      lineData[i] = 0;
    }
}

void Robot::start(int baudRate)
{
  Serial.begin(57600);
  
  // tell the serial connect hello
  Serial.print(HANDSHAKE_TO);
  
  int i = 0;
  char reply[5];
  
  while(1){
    while (Serial.available()) {
      reply[i] = (char)Serial.read();
      Serial.write(reply[i]);
      i++;
    }
    if (i==5){
      break;
    } else {
      delay(10);
    }
  }
  
  if (strcmp(reply, HANDSHAKE_FROM)){
    digitalWrite(13,HIGH);
  }

}

