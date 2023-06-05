#!/usr/bin/env python3
from std_msgs.msg import UInt16
import rospy
from main_package.srv import GetCommands, GetCommandsResponse
from std_msgs.msg import Bool
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage, Image
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import BatteryState
from std_msgs.msg import Bool, String
import serial
import struct
import time
import cv2
import zlib
import os


rospy.init_node("radio_receiver")

list_btn = [0]

data = list()
data_length = 0
ser = serial.Serial("/dev/ttyUSB0", 57600, timeout = 1)
ser.setDTR(False)

stop_pub = rospy.Publisher("/stop_topic", Bool, queue_size=3)
led_pub = rospy.Publisher("/led1", String, queue_size=1)
ser.dtr = False
ser.reset_input_buffer()
ser.reset_output_buffer()

cvBridge = CvBridge()
rospy.loginfo("success radio receiver init")

image_msg = Image()
pose = Pose2D()
bat_voltage = 0.
btn_state = False
can_change = True
list_data = [0,0,0,0,0,0,0]
def image_cb(img):
    global image_msg
    image_msg = img
    

def pose_cb(data):
    global pose
    pose = data
    
    
def bat_cb(data):
    global bat_voltage
    bat_voltage = data.voltage


def btn_cb(data):
    global btn_state
    global can_change
    if can_change:
        btn_state = data.data
    if btn_state:
        can_change = False
    state = String()
    state.data = 'on'
    led_pub.publish(state)
    

rospy.Subscriber("/front_camera/image_raw", Image, image_cb)
rospy.Subscriber("/odom_pose2d", Pose2D, pose_cb)
rospy.Subscriber("/bat", BatteryState, bat_cb)
rospy.Subscriber("/btn", Bool, btn_cb)

# def read_data():
#     # global data
#     # global data_length
#     # time.sleep(0.1)
#     # pack = list()
#     # cnt = 0
#     # for i in range(ser.in_waiting // 3):
#     #     format_str = (">3B")
#     #     if ser.in_waiting >= 3:
#     #         raw_command = struct.unpack(format_str, ser.read(size=3))
#     #         if raw_command == (255, 255, 255):
#     #             s = Bool()
#     #             s.data = True
#     #             stop_pub.publish(s)
#     #             pack = list()
#     #             cnt = 0
#     #             data = list()
#     #             data_length = 0
#     #             break
#     #         else:
#     #             s = Bool()
#     #             s.data = False
#     #             stop_pub.publish(s)
#     #         pack.extend(list(raw_command))
#     #         cnt += 1
#     # ser.reset_input_buffer()        
#     # return pack, cnt
#     pass


def handle_radio_receiver(req):
    global data
    global data_length
    resp = GetCommandsResponse()
    resp.commands_count = data_length
    resp.commands = data
    data = list()
    data_length = 0
    return resp


def get_frame():
    # TODO: encode frame with cobs
    # try:
    frame = cvBridge.imgmsg_to_cv2(image_msg, "bgr8")
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    resized_img = cv2.resize(frame, (100, 100))
    compressed_img = cv2.imencode('.jpg', resized_img)[1].tobytes()
    # mega_compressed_img = zlib.compress(compressed_img, level=-1)
    img_len = len(compressed_img)
    rospy.loginfo(img_len)
    # ser.write(b"BGN" + compressed_img + b"END")
    return compressed_img, img_len
    # except Exception:
    #     return 0
    
    
def get_meta():
    global can_change
    global btn_state
    ret = struct.pack('3df?', pose.x, pose.y, pose.theta, bat_voltage, btn_state)
    if btn_state:
        can_change = True
    # btn_state = False   
    return ret 
   

def read_answer():
    global data
    global data_length
    #time.sleep(0.25)
    begin_pack = ser.read_until(b"BGN") # BEGN
    raw_data = ser.read_until(b"END")[:-3]
    
    # rospy.loginfo(raw_data)
    commands = raw_data
    #print(commands)
    data.extend(commands)
    data_length += len(commands)
    
    





def capture(img):
    try:
        f = open('/home/pi/catkin_ws/src/main_package/src/img123.jpeg', 'wb+')
        f.write(img.data)
    except:
        print('error take img')
    
def callback_bat(data):
    
    a = data.voltage
    
    list_data[0]=a
    
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/bat", BatteryState, callback_bat)



def get_photo():


    frame = cvBridge.imgmsg_to_cv2(image_msg, "bgr8")
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    resized_img = cv2.resize(frame, (100, 100))
    compressed_img = cv2.imencode('.jpg', resized_img)[1].tobytes()

    img_len = len(compressed_img)
    rospy.loginfo(img_len)

    return compressed_img, img_len


def callback_led(data):
    global start_led
    start_led = data.data
    
    list_btn[0] = start_led #znachenie led na rovere




            
def main():
    global data
    global data_length
    get = False
    flag_not_start = True
    letsGo=False
    time.sleep(1)
    s = rospy.Service("RadioReceiver", GetCommands, handle_radio_receiver)
    rospy.Subscriber("led", UInt16, callback_led)
    #rospy.Subscriber("/front_camera/image_raw/compressed", CompressedImage, capture)
    
    
    
    
    while not rospy.is_shutdown():

        if list_btn[0] == 1 and flag_not_start:
            for i in range(3):
                ser.write(b'start')
                time.sleep(1)
            flag_not_start = False

        
        elif not flag_not_start and list_btn[0] == 1:
                
            
            
            data_of_photo, img_len = get_photo()

            
            
            
            for i in range(img_len // 512):  #512
                start = time.time()
                ser.write(data_of_photo[512*i:512*(i+1)])
                #time.sleep(0.5)
                #print(data_of_photo[512*i:512*(i+1)])
                #print((len(data_of_photo[512*i:512*(i+1)]))* (i+1))
                print()
                read_answer()

                print(time.time()-start)
            ost = img_len%512
            if ost!=0:
                ser.write(data_of_photo[-ost:])
                read_answer()
            ser.write(b'end')
            
            read_answer()
        elif not flag_not_start and list_btn[0] == 0:
            time.sleep(3)

            for i in range(3):
                ser.write(b'stop')
                print('send stop')
                time.sleep(1)
            flag_not_start = True

        else:
            print(list_btn)

        



if __name__ == "__main__":
    main()

