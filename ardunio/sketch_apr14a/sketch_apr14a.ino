#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle nh;
const int buttonPin = 2;
std_msgs::String str_msg;
ros::Publisher chatter("btn", &str_msg);
int buttonState = 0;



void setup()
{
  pinMode(buttonPin, INPUT);
  nh.initNode();
  nh.advertise(chatter);
}

void loop()
{
  buttonState = digitalRead(buttonPin);
  
  if (buttonState == HIGH) {   
    str_msg.data = "0";
  }
  else if (buttonState == LOW){

    str_msg.data = "1";
  }

  
  chatter.publish( &str_msg );
  nh.spinOnce();
}
