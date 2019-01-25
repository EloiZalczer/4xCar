#include <Servo.h>

String command = "";
bool received = false;
Servo servo;
Servo brushless;

void setup(){
  Serial.begin(115200);
  command.reserve(3);
  servo.attach(9);
  brushless.attach(11);
}

void loop(){
  if(received){
    control_motors(command[0], command[1]);
    command = "";
    received = false;
  }
}

void serialEvent(){
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();

    command += inChar;

    if (inChar == 0) {
      received = true;
    }
  }
}

void control_motors(char direction, char speed){
  servo.write((unsigned int)direction);
  brushless.write((unsigned int)speed);
}
