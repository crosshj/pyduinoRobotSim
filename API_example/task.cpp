#define NUMBER_OF_SENSORS 4
#define TOKEN "_TASK"

#include "Robot.h"
#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "string.h"
#include "Wire.h"

int Robot::pollTask(){
  int state = 1;
  int i=0;

  // signal host that we want task status
  Serial.print(TOKEN);

  for (int i=0; i < NUMBER_OF_SENSORS; i++)
  {
      taskData[i] = 0;
  }
  
  // connect to task 1 using WIRE (later will be using xbee shield)
  Wire.requestFrom(4, 1);

  int written = 0;
  while(1){
    while(Wire.available())
    {
      byte temp = Wire.read(); 
      taskData[0] =  int(temp) - 101;
      written = 1;
    }
    if (written == 1){
      break;
    }
  }

  // this while loop should not go on forever
  // should include a way of keeping track of time spent
  // and conditionally break
  while(1){
    while (Serial.available()) {
      if (i != 0){
        taskData[i] = (char) Serial.read();
      } else {
        char temp = (char) Serial.read();  // throw away for task 0 
      }
      Serial.print(taskData[i]);
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
