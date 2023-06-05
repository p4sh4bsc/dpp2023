import struct
import serial
import time

import rospy
from std_msgs.msg import String



pub = rospy.Publisher('btn', String, queue_size=10)
rospy.init_node('talker', anonymous=True)


if __name__ == '__main__':

    print(1)
    ser = serial.Serial('/dev/ttyUSB0', 38400)
    ser.setDTR(False)
    param = '0'
    command = str(input("aga: "))
    if command == "pot":
        while True:

            s = ser.readline()
            str_line = s.decode("utf-8")
            param = str_line[0:4]
            print(param)
    else:
        while True:

            s = ser.readline()
            str_line = s.decode("utf-8")
            param = str_line[0:1]
            print(param)
            pub.publish(param)
