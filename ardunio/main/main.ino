
#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;
std_msgs::String str_msg_btn;

ros::Publisher btn("btn", &str_msg_btn);
ros::Publisher led("led", &str_msg_led);


void setup() {
  
  pinMode(2, INPUT);      //btn
  pinMode(A1, INPUT);     //pot_1
  pinMode(A2, OUTPUT);    //led
  nh.initNode();
  nh.advertise(btn);
  nh.advertise(led);
}
 
void loop(){
  
  int rotat, led, btn;

 

  rotat_pot_1 = analogRead(A1);


  if (buttonState == HIGH) {   
    btn = 1;
    led = 1;
    digitalWrite(A2, HIGH);
    str_msg_btn.data = 1;
    str_msg_led.data = 1;
  }
  else {
    btn = 0;
    led = 0;
    digitalWrite(A1, HIGH);
    str_msg_btn.data = 0;
    str_msg_led.data = 0;
  }

  
  btn.publish( &str_msg_btn );
  led.publish( &str_msg_led );
  nh.spinOnce();
  
}
