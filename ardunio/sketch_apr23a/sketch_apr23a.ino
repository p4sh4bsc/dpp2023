#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo360;
Servo servo180_p;


void setup() {
  // put your setup code here, to run once:

  servo1.attach(46);   //serva forw back
  servo2.attach(45);  //serva up down
  servo360.attach(10); //serva Zahvat
  servo180_p.attach(44);
  

}

void loop() {
  // put your main code here, to run repeatedly:

  servo1.write(90);
  delay(1000);
  servo2.write(45);
  delay(1000);
  servo360.write(90);
  delay(1000);
  servo180_p.write(45);
  delay(1000);
  
  delay(3000);
    
  
  servo1.write(0);
  delay(1000);
  servo2.write(180);
  delay(1000);
  servo360.write(90);
  delay(1000);
  servo180_p.write(90);
  delay(1000);
}
