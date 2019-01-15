String command = "";
bool received = false;

int servo = 9; //TODO
int brushless = 10; //TODO

void setup() {
  // initialize serial:
  Serial.begin(9600);
  command.reserve(2);
}

void loop() {
  if(received){
    analogWrite(servo, command[0]);
    analogWrite(brushless, command[1]);
    command = "";
    received = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();

    command += inChar;

    if (inChar == '\n') {
      received = true;
    }
  }
}
