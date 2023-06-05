#!/usr/bin/env python3

import rospy
import serial
import struct
import time

rospy.init_node("radio_receiver")


ser = serial.Serial('/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.2:1.0-port0', 38400, timeout=0.2)
ser.setDTR(False)



def main():
    while not rospy.is_shutdown():
        time.sleep(0.1)
        if ser.inWaiting() > 4:
            begin_pack = ser.read(4).decode('utf-8') # BEGN
            if begin_pack == "BEGN":
                data = ser.read_until(b"END")[:-3]
                (i,), data = struct.unpack("I", data[:4]), data[4:]
                s = data[:i]
                hw_string = s.decode('utf-8')
                rospy.loginfo(hw_string)
            ser.reset_input_buffer()


if __name__ == "__main__":
    main()