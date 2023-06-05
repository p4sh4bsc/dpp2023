#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

rospy.init_node("test_subscriber")

def hellow_world_cb(data):
    rospy.loginfo(data.data)


rospy.Subscriber("/hellow_world", String, hellow_world_cb)

def main():
    while not rospy.is_shutdown():
        pass


if __name__ == "__main__":
    main()