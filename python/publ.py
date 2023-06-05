#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import termios
import tty
import sys
from select import select

rospy.init_node("test_publisher")

string_pub = rospy.Publisher('/hellow_world', String, queue_size=3)
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=3)
cmd_vel_msg = Twist()
cmd_vel_msg.linear.x = 0.1
hellow_world_msg = String()
hellow_world_msg.data = "Hello from main"


def getKey(settings, timeout):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def main():
    while not rospy.is_shutdown():
        key = getKey(termios.tcgetattr(sys.stdin), 0.5)
        if key == 'w':
            cmd_vel_pub.publish(cmd_vel_msg)
        else:
            cmd_vel_pub.publish(Twist())
        string_pub.publish(hellow_world_msg)
        
        


if __name__ == "__main__":
    main()
    
    