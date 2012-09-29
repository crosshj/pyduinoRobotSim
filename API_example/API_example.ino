#include <HardwareSerial.h>
#include <Wire.h>
#include "Robot.h"

Robot myRobot;   

void setup(){
  myRobot.start(57600);
  pinMode(13, OUTPUT);
}

// length for delays on differing sections of track
int BIG1 = 5575;
int L1 = 1390;
int L2 = 630;
int L3 = 1090;
int L4 = BIG1-2*L1-2*(L3);
int L5 = 2535;

void loop(){
  
  // this works, but I'm not really doing anything with it here 
  myRobot.pollLine();

  // at first of course, get sensor values
  myRobot.pollTask();
  
  // the following are direction functions that are
  // implemented below
  left(L1);  
  
  // decide
  if (myRobot.taskData[0]){
    up(L2);
  } else {
    down(L2); 
  }
  left(L3);
  if (myRobot.taskData[0]){
    down(L2);
  } else {
    up(L2); 
  }  left(L4);
  
  //decide
  if (myRobot.taskData[1]){
    up(L2);
  } else {
    down(L2); 
  }
  left(L3);
  if (myRobot.taskData[1]){
    down(L2);
  } else {
    up(L2); 
  }
  left(L1);
  up(L5);
  right(L1);
  
  //decide
   if (myRobot.taskData[2]){
    up(L2);
  } else {
    down(L2); 
  }
  right(L3);
  if (myRobot.taskData[2]){
    down(L2);
  } else {
    up(L2); 
  }
  right(L4);
  
  //decide
  if (myRobot.taskData[3]){
    up(L2);
  } else {
    down(L2); 
  }
  right(L3);
  if (myRobot.taskData[3]){
    down(L2);
  } else {
    up(L2); 
  }
  right(L1);
  down(L5);
  
  halt();
  
  // END OF LAP
}


void left(int time){
    if ( myRobot.motor(255,255,255,255,0) )
    {
      delay(time);
      digitalWrite(13,HIGH);
    } else {
      myRobot.motor(0,0,0,0,0);
      delay(1000); 
    }
}

void up(int time){
    if ( myRobot.motor(-255,255,255,-255,0) )
    {
      delay(time);
      digitalWrite(13,HIGH);
    } else {
      myRobot.motor(0,0,0,0,0);
      delay(1000); 
    }
}

void right(int time){
    if ( myRobot.motor(-255,-255,-255,-255,0) )
    {
      delay(time);
      digitalWrite(13,HIGH);
    } else {
      myRobot.motor(0,0,0,0,0);
      delay(1000); 
    }
}

void down(int time){
    if ( myRobot.motor(255,-255,-255,255,0) )
    {
      delay(time);
      digitalWrite(13,HIGH);
    } else {
      myRobot.motor(0,0,0,0,0);
      delay(1000); 
    }
}

void halt(){
    if ( myRobot.motor(0,0,0,0,0) )
    {
      digitalWrite(13,HIGH);
    } else {
      myRobot.motor(0,0,0,0,0);
      delay(1000); 
    }
}

