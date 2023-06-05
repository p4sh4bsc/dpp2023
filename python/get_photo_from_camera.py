import rospy
from sensor_msgs.msg import CompressedImage

from sensor_msgs.msg import BatteryState


def capture(img):
    rospy.loginfo(img.format)
    print(img.format)

    
    f = open('img3.jpeg', 'wb+')
    f.write(img.data)


if __name__ == "__main__":
    
    rospy.init_node('camera')
    rospy.Subscriber("/front_camera/image_raw/compressed", CompressedImage, capture)
    rospy.spin()
