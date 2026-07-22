#include <Servo.h>

Servo penServo;

const int SERVO_PIN = 9;
const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;

String inputBuffer = "";

void setup() {
  Serial.begin(9600);
  penServo.attach(SERVO_PIN);
  penServo.write(90);
}

void loop() {
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      int angle = inputBuffer.toInt();
      angle = constrain(angle, MIN_ANGLE, MAX_ANGLE);
      penServo.write(angle);
      inputBuffer = "";
    } else {
      inputBuffer += c;
    }
  }
}