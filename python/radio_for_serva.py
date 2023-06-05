import struct
import serial
import time
import os
import rospy
from std_msgs.msg import String
from std_msgs.msg import UInt16


pub2 = rospy.Publisher('servo', UInt16, queue_size=10)
rospy.init_node('talker', anonymous=True)


if __name__ == '__main__':

    print(1)
    ser = serial.Serial('/dev/ttyUSB0', 38400)
    ser.setDTR(False)
    param = '0'
    while True:
    
        s = ser.readline()
        str_line = s.decode("utf-8")
        param = str_line.strip()
        print(param)
        print(list(param))
        param = int(int(param)//2.85)
        print(param)
        pub2.publish(param)


