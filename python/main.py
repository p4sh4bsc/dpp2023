#!/usr/bin/env python3

import rospy
import serial
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import UInt16
from std_msgs.msg import Int16, String
from tf.transformations import quaternion_multiply, quaternion_inverse, euler_from_quaternion
from main_package.srv import GetCommands
from std_msgs.msg import Bool
import math
import time

rospy.init_node("main")

global extra_stop
global odom
odom = Odometry()
stop = Bool()
stop_flag = 0
list_btn = [0, 0, 0]

def odom_cb(data):
    global odom
    odom = data

def stop_cb(data):
    global stop
    print(data)
    stop = data


rospy.Subscriber("/odom", Odometry, odom_cb)
rospy.Subscriber("/stop_topic", Bool, stop_cb)
cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=3)
led_pub = rospy.Publisher("/led1", String, queue_size=3)
rospy.loginfo("success main init")


def get_degree_diff(prev_orientation, current_orientation):
        prev_q = [prev_orientation.pose.pose.orientation.x, prev_orientation.pose.pose.orientation.y,
                  prev_orientation.pose.pose.orientation.z, prev_orientation.pose.pose.orientation.w]
        current_q = [current_orientation.pose.pose.orientation.x, current_orientation.pose.pose.orientation.y,
                     current_orientation.pose.pose.orientation.z, current_orientation.pose.pose.orientation.w]
        delta_q = quaternion_multiply(prev_q, quaternion_inverse(current_q))
        (_, _, yaw) = euler_from_quaternion(delta_q)
        ans = math.degrees(yaw)

        return ans


def get_distance(start_pose, current_pose):
    return math.sqrt(math.pow(start_pose.x - current_pose.x, 2) + math.pow(start_pose.y - current_pose.y, 2))


def move(x,z):
    pub_1_vel = Twist()
    pub_1_vel.linear.x = x
    pub_1_vel.angular.z = z
    cmd_vel_pub.publish(pub_1_vel)


def turn_around(vec, angle, v, soft):
    global odom
    rospy.sleep(0.5)
    angle = angle - 4 if not soft else angle
    start_orientation = odom
    v *= vec
    current_angle = abs(get_degree_diff(start_orientation, odom))
    while not rospy.is_shutdown() and not stop.data and current_angle < angle:
        current_angle = abs(get_degree_diff(start_orientation, odom))
        print(current_angle, angle)
        x = 0
        z = v
        move(x, z)
        rospy.sleep(0.05)

    move(0, 0)
    rospy.loginfo("angular_stop")
    rospy.sleep(0.1)


def turn_forward(v, l):
    global odom
    time.sleep(0.2)
    start_pose = odom
    current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
    l += current_distance
    while not rospy.is_shutdown() and not stop.data and current_distance <= l:
        current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
        #print(odom)
        print(current_distance,l)
        x = v
        z = 0
        move(x, z)
        rospy.sleep(0.1)
    x = 0
    z = 0
    move(x, z)
    rospy.loginfo("forward_stop")
    rospy.sleep(0.1)



def start():
    d = UInt16()
    d.data = 90
    rospy.loginfo(d)



def callback_stop(data):
    global extra_stop

    extra_stop = data.data
    list_btn[0] = extra_stop
    
    
def callback_start(data):
    global start_info
    start_info = data.data
    
    list_btn[1]=start_info



def find():
    rospy.init_node('list', anonymous=True)
    rospy.Subscriber("/extra_stop", UInt16, callback_stop)
    #rospy.spin()

def check_led():
    rospy.init_node('check_led', anonymous=True)
    rospy.Subscriber("/led", UInt16, callback_stop)




def callback_led(data):
    global start_led
    start_led = data.data
    
    list_btn[2] = start_led #znachenie led na rovere

def main():
    global commands
    start_flag = False    
    
    
    
    ###проверить вызов функции find
    
    rospy.Subscriber("extra_stop", UInt16, callback_stop)
    #rospy.Subscriber("btn", UInt16, callback_start)
    rospy.Subscriber("led", UInt16, callback_start)
    
    
    pub_serv_forw_back = rospy.Publisher('servo_forw_back', UInt16, queue_size=10) #9 PIN forw back
    pub_serv_up_down = rospy.Publisher('servo_up_down', UInt16, queue_size=10)     #10 PIN up down
    pub_serv360 = rospy.Publisher('servo360', UInt16, queue_size=10)               #8 PIN
    pub_serv180_p = rospy.Publisher('servo180_p', UInt16, queue_size=10)
    
    pub_shagRight = rospy.Publisher('shagRight', UInt16, queue_size=10)
    pub_shagLeft = rospy.Publisher('shagLeft', UInt16, queue_size=10)
    
    #rospy.init_node('servo_node', anonymous=True)
    
    commands_list = [0,0,0,0,0,0,0]
    rospy.wait_for_service("RadioReceiver")
    data_reader = rospy.ServiceProxy("RadioReceiver", GetCommands)
    velocity = 0.2
    
    x = 0
    y = 0
    while not rospy.is_shutdown():
        
        
        
        
        try:

            
            raw_data = data_reader(1)
            if raw_data.commands_count > 0:
                try:
                    commands = raw_data.commands
                    rospy.loginfo(commands)
                    commands_line = commands.decode()

                    commands_list_pre = list(map(int, commands_line.split()))
                    print(commands_list_pre)
                    
                    print(list_btn)
                    
                    
                    # WS #
                    if commands_list_pre[3] == 1023:
                        x = velocity
                        rospy.loginfo('forward')
                    elif commands_list_pre[3] == 0:
                        x = -velocity
                        rospy.loginfo('backward')
                    else:
                        x = 0
                        rospy.loginfo('stop')
                        
                        
                        
                    # RL #
                    if commands_list_pre[4] == 0:
                        y = velocity
                        rospy.loginfo('right')
                    elif commands_list_pre[4] == 1023:
                        y = -velocity
                        rospy.loginfo('left')
                    else:
                        y = 0
                        rospy.loginfo('stop')
                    
                    print(1)
                    
                    angle_for_servo1 = commands_list_pre[0]//10.8
                    angle_for_servo2 = commands_list_pre[1]//7.85
                    angle_for_servo3 = commands_list_pre[2]//5.69
                        
                        
                    
                    if commands_list_pre[5] == 1 and commands_list_pre[6] == 1:
                        pub_serv360.publish(int(90))
                    elif commands_list_pre[6] == 0:
                        pub_serv360.publish(int(180))
                    elif commands_list_pre[5] == 0:
                        pub_serv360.publish(int(0))
                        
                    
                    if commands_list_pre[7] == 1:
                        pub_serv180_p.publish(int(90))
                    else:
                        pub_serv180_p.publish(int(angle_for_servo3))
                        
                        
                        
                    print('after if')
                    
                    
                    
                    
                    pub_serv_forw_back.publish(int(angle_for_servo1))
                    pub_serv_up_down.publish(int(angle_for_servo2))
                    
                    
                        
                    print('pls')
                    
                    if list_btn[0] == 1:
                        x = 0
                        y = 0
                    
                    move(x, y)
                    print('after func')
                except Exception as ex:
                    print(ex)
                #if list_btn[0] == 1:
                #        x = 0
                #        y = 0
                        
                        
                
                
        except Exception as ex:
            print(ex)
   
                    


if __name__ == "__main__":
	start()
	main()

