#include "functions.h"

// define flags
int FLAG_PRE_BALL = 0;  // 0 ball is not covered by door, 1 ball is covered by door

// init receive from Python
int servo_pos_py;
int turn_mode_py;
double PID_left_right_py;
double max_speed_py;
int wall_follow_py;

// servo motor
Servo servo996;  // servo object representing the MG 996R servo
int servo_degree;

// ball count
int ball_count = 3;
int pre_ball_count = 0;

// sonar distance
int sonar_r = 0;
int sonar_l = 0;
int sonar_f = 0;

void setup() {
  Serial.begin(9600);

  pinMode(start_pin, INPUT);
  pinMode(mot_pwm_r, OUTPUT);
  pinMode(mot_for_r, OUTPUT);
  pinMode(mot_rev_r, OUTPUT);
  pinMode(mot_pwm_l, OUTPUT);
  pinMode(mot_for_l, OUTPUT);
  pinMode(mot_rev_l, OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(trig_rlf, OUTPUT);
  pinMode(echo_r, INPUT);
  pinMode(echo_l, INPUT);
  pinMode(echo_f, INPUT);

  servo996.attach(ser_mot);
  servo_degree = ServoControl(SERVO_INIT, servo996);
}

void loop() {
  // get sonar distances
  sonar_r = SonarDist(trig_rlf, echo_r);
  sonar_l = SonarDist(trig_rlf, echo_l);
  sonar_f = SonarDist(trig_rlf, echo_f);

  // send the distances to python for decision making
  Serial.print(sonar_r);
  Serial.print(",");
  Serial.print(sonar_l);
  Serial.print(",");
  Serial.print(sonar_f);
  Serial.print(",");
  Serial.println(ball_count);
  Serial.flush();
  delay(50);
  // FlushReadData();
  
//  int trigger = 1;
//  Serial.println(trigger);
//  // FlushReadData();
//  delay(50);

  // receive data from python
  bool dataIsValid = false;  // This flag checks the validity of the data

  // Loop until valid data is received
  while (!dataIsValid) {
    if (Serial.available() > 0) {
      String receivedData = Serial.readStringUntil('\n');
      Serial.flush();  // Clear the serial buffer to ensure fresh read next time

      // Check if the data starts with the expected symbol
      if (receivedData.startsWith("Y")) {
        // Remove the start symbol for further processing
        receivedData.remove(0, 1);  // Remove the first character

        // Validate and parse the data
        if (validateData(receivedData)) {
          parseData(receivedData);
          dataIsValid = true;  // Set the flag to true when data is valid
        } else {
          Serial.println("Error: Data is incorrect or incomplete.");
          delay(500);  // Optional: delay before next read attempt
        }
      } else {
        Serial.println("Error: Data does not start with the correct symbol.");
        delay(500);  // Optional: delay before next read attempt
      }
    }
    delay(10);  // Small delay to prevent overwhelming the CPU
  }
  
  if (servo_degree == SERVO_INIT){
    if (wall_follow_py) {
      // motor control for wall following
      // servo_degree = CloseDoor(servo996);
      if (turn_mode_py == 1) {  // normal turn
        MotorControlPID(PID_left_right_py, max_speed_py);
      } else if (turn_mode_py == 0) {  // stop
        MotorControlPID(PID_left_right_py, 0);
      } else if (turn_mode_py == -1) {  // tank turn
        MotorControlTankTurn(int(PID_left_right_py));
      }
    } else if (FLAG_PRE_BALL) {
      MotorControlPID(PID_left_right_py, max_speed_py);
    } else if (!wall_follow_py) {
      // motor and servo control for ball pick
      MotorControlPID(PID_left_right_py, max_speed_py);
      if (servo_pos_py == 1) {
        servo_degree = ServoControl(SERVO_ROT, servo996); // wrong value from raspberry pi
        servo_degree = SERVO_ROT;
        FLAG_PRE_BALL = 1;
      }
    }
  }else if (servo_degree == SERVO_ROT) { // close door after the door is open 
      servo_degree = CloseDoorBySonar(servo996);
      MotorControlPID(0, 0.3);
      servo_degree = CloseDoorBySonar(servo996);
    if (servo_degree == SERVO_INIT) {
      ball_count++;
      FLAG_PRE_BALL = 0;
      MotorControlPID(0, 0);
      delay(1000);
    }
    
  }
  //FlushReadData();
  delay(10);
  // Serial.println(ball_count);
}

bool validateData(String data) {
  // Implement validation logic here, e.g., checking for number of delimiters
  return (data.length() > 0 && data.indexOf(';') != -1);
}

void parseData(String data) {
  char str[100];
  data.toCharArray(str, 100);
  char* p = strtok(str, ";");
  int params[5];
  int i = 0;
  while (p != NULL && i < 5) {
    params[i++] = atof(p);
    p = strtok(NULL, ";");
  }

  if (i == 5) {
    servo_pos_py = params[0];
    turn_mode_py = params[1];
    PID_left_right_py = params[2];
    max_speed_py = params[3];
    wall_follow_py = params[4];
    Serial.println("Data successfully parsed and validated.");
  } else {
    Serial.println("Error: Incomplete data received.");
  }
}

void performActionsBasedOnData() {
  // Add your action code here
  Serial.println("Performing actions based on received data.");
}
