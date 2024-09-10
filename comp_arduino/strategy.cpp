#include "strategy.h"

int CloseDoorBySonar(Servo servo) {
  float distance = SonarSensor(1);
 Serial.print("Sonar:");
 Serial.println(distance);
  if (distance <= SONOR_THRE_BALL ) { // || (distance <= SONAR_THRE_BALL_WEIRD3 && distance >= SONAR_THRE_BALL_WEIRD2   distance <= SONOR_THRE_BALL
    delay(10);
    int servo_degree = ServoControl(SERVO_INIT, servo);
    distance = SonarSensor(0);
    delay(10);
    return SERVO_INIT;
  } else {
    return SERVO_ROT;  //signal not close the door
  }
}

int OpenDoor(Servo servo) {
  int servo_degree = ServoControl(SERVO_ROT, servo);
  delay(10);
  float distance = SonarSensor(0);
  return SERVO_ROT;
}

int CloseDoor(Servo servo) {
  int servo_degree = ServoControl(SERVO_INIT, servo);
  delay(10);
  float distance = SonarSensor(0);
  return SERVO_INIT;
}
