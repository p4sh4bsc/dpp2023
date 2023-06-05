#!/usr/bin/env python3

import rospy
import serial
import struct
import time
from std_msgs.msg import UInt16

rospy.init_node("radio_receiver")


ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', 38400, timeout=0.2)
ser.setDTR(False)

servo_pub = rospy.Publisher('/servoupdown', UInt16, queue_size=3)

def main():
    while not rospy.is_shutdown():
        time.sleep(0.1)
        if ser.inWaiting() > 3:
            begin_pack = ser.read(3)  # BEGN
            if begin_pack == b"BGN":
                data = ser.read_until(b"END")[:-3]
                data = data[0]
                rospy.loginfo(data)
                d = UInt16()
                d.data = data
                servo_pub.publish(d)
            ser.reset_input_buffer()


if __name__ == "__main__":
    main()