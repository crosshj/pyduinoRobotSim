#define NUMBER_OF_MOTORS 16
#define TOKEN "_MOTO"

#include "Robot.h"
#if defined(ARDUINO) && ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

#include "string.h"


int Robot::motor(int motor1, int motor2, int motor3, int motor4, int time){
  int state = 1;
  int i=0;
  
  motor1 = ((motor1+1)/2)+127;
  motor2 = ((motor2+1)/2)+127;
  motor3 = ((motor3+1)/2)+127;
  motor4 = ((motor4+1)/2)+127;
  
  // convert -255 to 255 into 0 to 255
  char new_motorData[4] = { motor1, motor2, motor3, motor4 };
  
  	// number - motor number
	// -255 <= speed <= 255, 0 is brake
	// time - if 0, then no timeout, otherwise

	//      (1)-----(2)
	//       |       |
	//       |       |
	//      (3)-----(4)

  // signal host that we want to do motors
  Serial.print(TOKEN);
 
  // wait for okay
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
 
  // if no reply then quit
  if (!strcmp(reply, "_OKAY")){
    return 0; 
  } 
   
 
  // send motor settings
  for(i=0; i<4; i++){
    Serial.print(new_motorData[i]);
  }

  // get a reply back
  i = 0;
  reply[5];
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
    for( i=0; i<4; i++){
      motorData[i] = ((new_motorData[i]-127)*2)-1;
    }
  } else {
    state = 0; 
  }

  return state;  // 1 for yes, 0 for no
}



