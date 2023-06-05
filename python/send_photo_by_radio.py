
import struct
import serial
import time
import cv2
import rospy
from sensor_msgs.msg import CompressedImage
import serial
import time
import cv2
from PIL import Image
import piexif
import os
from sensor_msgs.msg import BatteryState



list_data=[0, 0, 0]

class Coder:
    def code(a):
        #return struct.pack('>ch', bytes(a, encoding='utf-8'), int(b))
        return struct.pack('>ch', bytes(a, encoding='utf-8'))
    def decode(command):
        return struct.unpack('>ch', command)


def capture(img):
    try:
        f = open('img123.jpeg', 'wb+')
        f.write(img.data)
    except:
        print('error take img')
    
def callback_bat(data):
    a = data.voltage
    list_data[0]=a
    
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/bat", BatteryState, callback_bat)



if __name__ == '__main__':
    ser = serial.Serial("/dev/ttyUSB0", baudrate = 19200)
    ser.setDTR(False)
    time.sleep(2)
    
    #rospy.init_node('listener', anonymous=True)
    get = False
    
    rospy.Subscriber("/front_camera/image_raw/compressed", CompressedImage, capture)
    listener()
    while True:
        x = 0
        time.sleep(1)
        
        
        
        print(list_data)

        size_of_img = os.stat('img123.jpeg')
        
        while not get:
            if size_of_img.st_size <= 50:
                print('wait')
            else:
                get = True        
                
                
        dsize = (70, 70)

        
        originalImage = cv2.imread("img123.jpeg")
        new_size = cv2.resize(originalImage, dsize)
        cv2.imwrite("img_compresed.jpeg", new_size)
        grayImage = cv2.cvtColor(new_size, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("gray_img.jpeg", grayImage)

        

        
        image = Image.open('gray_img.jpeg')
        
        exif_ifd = {piexif.ExifIFD.UserComment: f'{list_data[0]}'.encode()}
        exif_dict = {"0th": {}, "Exif": exif_ifd, "1st": {}}
        exif_dat = piexif.dump(exif_dict)
        image.save('gray_img_with_exif.jpeg',  exif=exif_dat)


        #ser = serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0012-if00-port0", baudrate = 9600)

        
        data = open("gray_img_with_exif.jpeg","rb").read()
        
        data+=b'end'
        ser.write(data)
        print(data)
        print(len(data))
        time.sleep(2)

    

