#!/usr/bin/env python3

import rospy
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

global odom
odom = Odometry()
stop = Bool()


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



def main():
    rospy.wait_for_service("RadioReceiver")
    data_reader = rospy.ServiceProxy("RadioReceiver", GetCommands)
    velocity = 0.1
    x = 0
    y = 0
    while not rospy.is_shutdown():
        raw_data = data_reader(1)
        if raw_data.commands_count > 0:
            commands = raw_data.commands
            rospy.loginfo(commands)
            # WS #
            if commands[0] == 1:
                x = velocity
                rospy.loginfo('forward')
            elif commands[0] == 2:
                x = -velocity
                rospy.loginfo('backward')
            else:
                x = 0
                rospy.loginfo('stop')
                
                
                
            # RL #
            
            
            
            
            if commands[1] == 1:
                y = velocity
                rospy.loginfo('right')
            elif commands[1] == 2:
                y = -velocity
                rospy.loginfo('left')
            else:
                y = 0
                rospy.loginfo('stop')
            move(x, y)
            
                    


if __name__ == "__main__":
	start()
	main()
