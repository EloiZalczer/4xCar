#include <Servo.h>

Servo brushless;
int mode = 0;
boolean sent = false;


void setup(){
  Serial.begin(9600);
  brushless.attach(11);
}

void loop(){
  if(!sent){
    if(mode == 1){
      brushless.write(90);
      Serial.println("Neutral point");
    }
    else if(mode == 2){
      brushless.write(180);
      Serial.println("Full throttle");
    }
    else if(mode == 3){
      brushless.write(0);
      Serial.println("Full brake");
    }
    sent = true;
  }
}

void serialEvent(){
  while(Serial.available()){
    char inChar = (char)Serial.read();
    
    if(inChar = '1'){
      mode++;
      sent=false;
    }
  }
}
