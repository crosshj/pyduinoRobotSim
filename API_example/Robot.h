/*
  robot.h - Library for interfacing with robot
*/

#include <Wire.h>
#define HANDSHAKE_TO "PY>>>"
#define HANDSHAKE_FROM "PY<<<"

#ifndef Robot_h
#define Robot_h


class Robot
{
  public:
    char lineData[16];
    int motorData[4];
    char taskData[4];
        
    Robot(void);
    void start(int baudRate);
    int pollTask(void);
    int pollLine(void);
    int motor(int motor1, int motor2, int motor3, int motor4, int time);
};

#endif
