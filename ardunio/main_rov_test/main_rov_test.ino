
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/UInt16.h>
#include <Servo.h> 

ros::NodeHandle nh;

std_msgs::UInt16 str_msg_btn;
std_msgs::UInt16 str_msg_led;
std_msgs::UInt16 str_msg_stop;



ros::Publisher btn("btn", &str_msg_btn);
ros::Publisher led("led", &str_msg_led);
ros::Publisher extra_stop("extra_stop", &str_msg_stop);


int rotat_pot_1;
int led_info;
int btn_info = 0;
int stop_me = 0;
int incomingByte;

bool buttonState;
bool buttonStart;


Servo servo1;
Servo servo2;
Servo servo360;


void servo_cb_1( const std_msgs::UInt16& cmd_msg){
  servo1.write(cmd_msg.data); //set servo angle, should be from 0-180  
}


void servo_cb_2( const std_msgs::UInt16& cmd_msg){
  servo2.write(cmd_msg.data); //set servo angle, should be from 0-180  
}


void servo_cb_360( const std_msgs::UInt16& cmd_msg){
  servo360.write(cmd_msg.data); //set servo angle, should be from 0-180  
}


ros::Subscriber<std_msgs::UInt16> sub1("servo1", servo_cb_1);
ros::Subscriber<std_msgs::UInt16> sub2("servo2", servo_cb_2);
ros::Subscriber<std_msgs::UInt16> sub360("servo360", servo_cb_360);


void setup() {

  nh.initNode();
  nh.advertise(btn);
  nh.advertise(led);
  nh.advertise(extra_stop);



  pinMode(2, INPUT);      //btn
  pinMode(A1, INPUT);     //pot_1
  pinMode(A2, OUTPUT);    //led
  pinMode(2, INPUT);     //conts open
  pinMode(3, INPUT);     //conts close
  digitalWrite(A2, LOW);



  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub360);

  
  servo1.attach(9);
  servo2.attach(10);
  servo360.attach(8);


  
  delay(1000);

}
 
void loop(){
  bool buttonState = digitalRead(3); //koncevik
  bool buttonStart = digitalRead(1); //turn on
  bool buttonOff = digitalRead(11); //turn off
 

  rotat_pot_1 = analogRead(A1);


  



  if (buttonState == HIGH) {   
    stop_me = 1;
    str_msg_stop.data = 1;
  }
  else {
    stop_me = 0;
    str_msg_stop.data = 0;
  }



  if (buttonStart == HIGH){
    str_msg_btn.data = 1; //topic btn
    str_msg_led.data = 1; //topic led
    }
  
  else if (buttonOff == HIGH){
    str_msg_btn.data = 0;
    str_msg_led.data = 0;
    }

    
  btn.publish( &str_msg_btn );
  led.publish( &str_msg_led );
  extra_stop.publish( &str_msg_stop );




  
  nh.spinOnce();
  
}
