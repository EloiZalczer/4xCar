int vcc = 0;       // variable to store the value coming from the sensor
int gnd = 0;
int cmd = 0;
int cmdPin = 11;
int vccPin = 10;
int gndPin = 9;

void setup() {
  Serial.begin(9600);
  
  pinMode(gndPin, OUTPUT);
  pinMode(vccPin, OUTPUT);
  pinMode(cmdPin, OUTPUT);
}

void loop() {
  vcc = analogRead(A1);    // read the value from the sensor
  gnd = analogRead(A2);
  cmd = analogRead(A3);
  
  digitalWrite(vccPin, HIGH);
  digitalWrite(gndPin, LOW);
  if(cmd > 300){
    digitalWrite(cmdPin, HIGH);
  }
  else{
    digitalWrite(cmdPin, LOW);
  }
  
  /*analogWrite(cmdPin, cmd);
  analogWrite(vccPin, vcc);
  analogWrite(gndPin, gnd);*/
  Serial.print("VCC : ");
  Serial.print(vcc);
  Serial.print(" GND : ");
  Serial.print(gnd);
  Serial.print(" CMD : ");
  Serial.println(cmd);
}
