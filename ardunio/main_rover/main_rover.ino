
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>
#include <Stepper.h>




ros::NodeHandle nh;

std_msgs::UInt16 str_msg_btn;
std_msgs::UInt16 str_msg_led;
std_msgs::UInt16 str_msg_stop;



ros::Publisher btn("btn", &str_msg_btn);
ros::Publisher led("led", &str_msg_led);
ros::Publisher extra_stop("extra_stop", &str_msg_stop);




int stop_me = 0;

bool buttonState;
int buttonStart = 0;

int buttonRight = 0;
int buttonLeft = 0;
int lastbuttonStart;
int ledState = LOW;  


bool start_flag = false;

Servo servo1;
Servo servo2;
Servo servo360;
Servo servo180_p;


void servo_cb_1( const std_msgs::UInt16& cmd_msg) {
  servo1.write(cmd_msg.data); //set servo angle, should be from 0-180
}


void servo_cb_2( const std_msgs::UInt16& cmd_msg) {
  servo2.write(cmd_msg.data); //set servo angle, should be from 0-180
}


void servo_cb_360( const std_msgs::UInt16& cmd_msg) {
  servo360.write(cmd_msg.data); //set servo angle, should be from 0-180
}

void servo_cb_180_p( const std_msgs::UInt16& cmd_msg) {
  servo180_p.write(cmd_msg.data); //set servo angle, should be from 0-180
}









ros::Subscriber<std_msgs::UInt16> sub1("servo_forw_back", servo_cb_1);
ros::Subscriber<std_msgs::UInt16> sub2("servo_up_down", servo_cb_2);
ros::Subscriber<std_msgs::UInt16> sub360("servo360", servo_cb_360);
ros::Subscriber<std_msgs::UInt16> sub180_p("servo180_p", servo_cb_180_p);





void setup() {

  nh.initNode();
  nh.advertise(btn);
  nh.advertise(led);
  nh.advertise(extra_stop);


  //servo1.write(110); //max 110  min  45          
  //servo2.write(25); //min 5  max 50  dlya back         max 65   min 25dlya forw
  servo360.write(90);
  servo180_p.write(90);
  
  //btn
  pinMode(A2, OUTPUT);    //led
  pinMode(11, INPUT);     //on led
  pinMode(7, INPUT);    //off led



  digitalWrite(A2, LOW);





  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub360);
  nh.subscribe(sub180_p);


  servo1.attach(46);   //serva forw back
  servo2.attach(4);  //serva up down
  servo360.attach(8); //serva Zahvat
  servo180_p.attach(44); //serva povorot




  delay(1000);

}

void loop() {
  lastbuttonStart = buttonStart;
  buttonState = digitalRead(11);
  buttonStart = digitalRead(7);
  



  ////////////////////////////////////////////////////

  if (buttonState == HIGH) {
    stop_me = 1;
    str_msg_stop.data = 1;
  }
  else if (buttonState == LOW) {
    stop_me = 0;
    str_msg_stop.data = 0;
  }


  //////////////////////////////////////////////////////


  if(lastbuttonStart == HIGH && buttonStart == LOW) {

 
    ledState = !ledState;

    digitalWrite(A2, ledState); 
  }



  ///////////////////////////////////////////////////////

  if (digitalRead(A2) == HIGH) {
    str_msg_led.data = 1;
  }
  else if (digitalRead(A2) == LOW) {
    str_msg_led.data = 0;
  }
  ///////////////////////////////////////////////////////


  

  extra_stop.publish( &str_msg_stop );

  btn.publish( &str_msg_btn );
  led.publish( &str_msg_led );
  
  nh.spinOnce();

}
