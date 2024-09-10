#ifndef _Strategies_h
#define _Strategies_h

#include "functions.h"

#define SONOR_THRE_BALL 50
#define SONAR_THRE_BALL_WEIRD 600
#define SONAR_THRE_BALL_WEIRD2 80
#define SONAR_THRE_BALL_WEIRD3 100

int CloseDoorBySonar(Servo servo);
int OpenDoor(Servo servo);
int CloseDoor(Servo servo);

#endif
