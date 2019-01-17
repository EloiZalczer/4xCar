#include <Servo.h>

Servo servo;

void setup(){
  Serial.begin(9600);
  servo.attach(9);
}

void loop(){
  Serial.println(60);
  servo.write(60);
  delay(500);
  Serial.println(120);
  servo.write(120);
  delay(500);
  /*servo.write(180);
  delay(500);
  servo.write(120);
  delay(500);
  servo.write(60);
  delay(500);
  servo.write(0);
  
  
  for (int position = 0; position <= 180; position+=1){
    servo.write(position);
    delay(100);
    Serial.println(position);
  }
  
  for(int position = 180; position >=0; position -=1){
    servo.write(position);
    delay(100);
    Serial.println(position);
  }*/
}
