#include "functions.h"

void Mot_r(int dir, int speed) {
  // 1 forward, 0 stop, -1 reverse
  if (dir == 1) {
    digitalWrite(mot_for_r, HIGH);
    digitalWrite(mot_rev_r, LOW);
    analogWrite(mot_pwm_r, speed);
  } else if (dir == 0) {
    digitalWrite(mot_for_r, LOW);
    digitalWrite(mot_rev_r, LOW);
    analogWrite(mot_pwm_r, speed);
  } else if (dir == -1) {
    digitalWrite(mot_for_r, LOW);
    digitalWrite(mot_rev_r, HIGH);
    analogWrite(mot_pwm_r, speed);
  }
}

void Mot_l(int dir, int speed) {
  // 1 forward, 0 stop, -1 reverse
  if (dir == 1) {
    digitalWrite(mot_for_l, HIGH);
    digitalWrite(mot_rev_l, LOW);
    analogWrite(mot_pwm_l, speed);
  } else if (dir == 0) {
    digitalWrite(mot_for_l, LOW);
    digitalWrite(mot_rev_l, LOW);
    analogWrite(mot_pwm_l, speed);
  } else if (dir == -1) {
    digitalWrite(mot_for_l, LOW);
    digitalWrite(mot_rev_l, HIGH);
    analogWrite(mot_pwm_l, speed);
  }
}

void MotorControlTankTurn(int dir) {
  // 0 stop, 1 right, -1 left
  if (dir == 1) {
    Mot_l(1, MAX_SPEED_L);
    Mot_r(-1, MAX_SPEED);
  } else if (dir == -1) {
    Mot_l(-1, MAX_SPEED_L);
    Mot_r(1, MAX_SPEED);
  } else {
    Mot_l(0, 0);
    Mot_r(0, 0);
  }
}

void MotorControlPID(double PID_output, double speed_ratio) {
  // control by PID
  int max_speed_loc = MAX_SPEED * speed_ratio;
  int max_speed_loc_l = MAX_SPEED_L * speed_ratio;
  
  if (PID_output >= 0) {
    // turn right
    int speed = max_speed_loc * (1.0 - PID_output);
    Mot_r(1, speed);
    Mot_l(1, max_speed_loc_l);
  } else if (PID_output < 0) {
    int speed = max_speed_loc_l * (1.0 + PID_output);
    // turn left
    Mot_r(1, max_speed_loc);
    Mot_l(1, speed);
  }
}

float SonarSensor(int turn_on) {
  if (turn_on) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    int duration = pulseIn(echoPin, HIGH);
    float distance = (duration * .343) / 2;
    delay(50);
    return distance;
  } else {
    digitalWrite(trigPin, LOW);
    return 0;
  }
}

int SonarDist(int trigger_pin, int echo_pin) {
  digitalWrite(trigger_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger_pin, LOW);

  int duration = pulseIn(echo_pin, HIGH);
  int distance = (duration * .343) / 2;
  delay(100);
  return distance;  // mm
}

int ServoControl(int degree, Servo servo) {
  servo.write(degree);
  return degree;
}

/*
    int servo_pos_py
    int turn_mode_py
    float PID_left_right_py
    float max_speed_py
*/

void AnalyzeSerialData_v2(String receivedData, int& servo_pos_py, int& turn_mode_py, double& PID_left_right_py, double& max_speed_py, int& wall_follow_py) {
  servo_pos_py = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);

  turn_mode_py = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);

  PID_left_right_py = receivedData.substring(0, receivedData.indexOf(';')).toFloat();
  receivedData.remove(0, receivedData.indexOf(';') + 1);

  max_speed_py = receivedData.substring(0, receivedData.indexOf(';')).toFloat();
  receivedData.remove(0, receivedData.indexOf(';') + 1);

  wall_follow_py = receivedData.toInt();
  delay(20);
}
void AnalyzeSerialData(String receivedData, int& forwardDist, int& leftDist, int& backDist, int& rightDist, int& ballCenterX, int& ballCenterY, int& ballDisCenter, int& xCenterCoor) {
  int partialData = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);  // remove analyzed part
  if (partialData != -1) {
    forwardDist = partialData;
  }
  partialData = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);
  if (partialData != -1) {
    leftDist = partialData;
  }
  partialData = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);
  if (partialData != -1) {
    backDist = partialData;
  }
  partialData = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);
  if (partialData != -1) {
    rightDist = partialData;
  }
  ballCenterX = receivedData.substring(0, receivedData.indexOf(',')).toInt();
  receivedData.remove(0, receivedData.indexOf(',') + 1);
  ballCenterY = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);
  ballDisCenter = receivedData.substring(0, receivedData.indexOf(';')).toInt();
  receivedData.remove(0, receivedData.indexOf(';') + 1);
  xCenterCoor = receivedData.toInt();
}

void FlushReadData() {
  while (Serial.read() >= 0) {}
}
/* used to be in .ino
  if (Serial.available() > 0) {
    // read from serial
    String receivedData = Serial.readStringUntil('\n');  // end with '\n'
    // print for test
    Serial.print("Received from Python: ");
    Serial.println(receivedData);

    // analyze data received
    AnalyzeSerialData(receivedData, forwardDist, leftDist, backDist, rightDist, ballCenterX, ballCenterY, ballDisCenter, xCenterCoor);

      // print for test
      Serial.print("Forward Distance: ");
    Serial.println(forwardDist);
    Serial.print("Left Distance: ");
    Serial.println(leftDist);
    Serial.print("Back Distance: ");
    Serial.println(backDist);
    Serial.print("Right Distance: ");
    Serial.println(rightDist);
    Serial.print("Ball Center X: ");
    Serial.println(ballCenterX);
    Serial.print("Ball Center Y: ");
    Serial.println(ballCenterY);
    Serial.print("Ball Distance Center: ");
    Serial.println(ballDisCenter);
    Serial.print("xCenterCoor Center: ");
    Serial.println(xCenterCoor);
  }
  */
