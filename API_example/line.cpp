#define NUMBER_OF_SENSORS 16
#define TOKEN "_LINE"
#include "Robot.h"
#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "string.h"


int Robot::pollLine(void)
{
  int state = 1;
  int i=0;

  for (int i=0; i < NUMBER_OF_SENSORS; i++)
  {
      lineData[i] = 0;
  }
  
  // signal host that we want task status
  Serial.print(TOKEN);

  
  // this while loop should not go on forever
  // should include a way of keeping track of time spent
  // and conditionally break
  while(1){
    while (Serial.available()) {
      lineData[i] = (char) Serial.read();
      Serial.print(lineData[i]);
      i++;
    }
    if (i==NUMBER_OF_SENSORS){
      break;
    } else {
      delay(10);
    }
  }
  
  i = 0;
  char reply[5];
  while(1){
    while (Serial.available()) {
      reply[i] = (char)Serial.read();
      i++;
    }
    if (i==5){
      break;
    } else {
      delay(10);
    }
  }
  
  
  if (strcmp(reply, TOKEN)){
    digitalWrite(13,LOW);
    state = 1;
  } else {
    state = 0; 
  }
  
  return state;

}

