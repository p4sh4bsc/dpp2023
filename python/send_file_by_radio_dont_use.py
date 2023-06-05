
import struct
import serial
import time
import cv2
import rospy
from sensor_msgs.msg import CompressedImage
import serial
import time
import cv2

class Coder:
    def code(self, a):
        #return struct.pack('>ch', bytes(a, encoding='utf-8'), int(b))
        return struct.pack('>ch', bytes(a, encoding='utf-8'))
    def decode(self, command):
        return struct.unpack('>ch', command)




if __name__ == '__main__':
    cd = Coder()
    originalImage = cv2.imread('img.png')
    print(len(open("img.png","rb").read()))
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
    #ser = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0012-if00-port0", baudrate = 9600)
    ser = serial.Serial("/dev/ttyUSB0", baudrate = 38400)
    ser.setDTR(False)
    
    cv2.imwrite('bw.png', grayImage)

    data = open("bw.png","rb").read()
    print(len(data))

    for i in range(3):
        ser.write(open("bw.png","rb").read())
    
    ser.write(b'\end')
    time.sleep(1)
        

