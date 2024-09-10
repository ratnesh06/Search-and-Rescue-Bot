#ifndef _Functions_h
#define _Functions_h

#include <Servo.h>
#include <Arduino.h>
#include "strategy.h"

// DC motor pin
#define mot_pwm_r 3
#define mot_rev_r 4
#define mot_for_r 2
#define mot_pwm_l 6
#define mot_for_l 7
#define mot_rev_l 5

// servo motor pin
#define ser_mot 11

// DC motor
#define MAX_SPEED 135
#define MAX_SPEED_L 135


// servo motor
#define SERVO_INIT 180
#define SERVO_ROT 90

// sonar sensor
#define trigPin A0
#define echoPin A1
#define trig_rlf A2
#define echo_r A5
#define echo_l A3
#define echo_f A4

// start button pin
#define start_pin 2


// function def
void Mot_r(int dir, int speed);
void Mot_l(int dir, int speed);
void MotorControlTankTurn(int dir);
void MotorControlPID(double PID_output, double speed_ratio);
float SonarSensor(int turn_on);
int SonarDist(int trigger_pin, int echo_pin);
void WallFollow(int threth_distance);
int ServoControl(int degree, Servo servo);
void AnalyzeSerialData_v2(String receivedData, int& servo_pos_py, int& turn_mode_py, double& PID_left_right_py, double& max_speed_py, int& wall_follow_py);
void FlushReadData();
void AnalyzeSerialData(String receivedData, int& forwardDist, int& leftDist, int& backDist, int& rightDist, int& ballCenterX, int& ballCenterY, int& ballDisCenter, int& xCenterCoor);


#endif
