#include <Servo.h>

Servo brushless;

void setup(){
  Serial.begin(9600);
  brushless.attach(11);
}

void loop(){
  
  for (int position = 0; position <= 180; position+=1){
    brushless.write(position);
    delay(100);
    Serial.println(position);
  }
  
  for(int position = 180; position >=0; position -=1){
    brushless.write(position);
    delay(100);
    Serial.println(position);
  }
}
