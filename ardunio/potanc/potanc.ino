
#include <ros.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle nh;

std_msgs::UInt16 std_msg;
ros::Publisher pub_button("angle", &std_msg);




void setup()
{
  nh.initNode();
  nh.advertise(pub_button);

  pinMode(A0, INPUT);


}

void loop()
{
  int rotat;
  rotat = analogRead(A0);
  std_msg.data = rotat;
  //pub_button.publish(&rotat);
  pub_button.publish(&std_msg);


  delay(1000);

  nh.spinOnce();
}
