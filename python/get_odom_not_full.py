import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

from sensor_msgs.msg import BatteryState
global a


listX = [0,0,0]
def callback(data):
    
    #rospy.loginfo(data.voltage)
    
    a = data.voltage

    listX[0] = a
    
def listener():


    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/bat", BatteryState, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    listener()
    while True:
        
        print(listX)

    #print(rospy.Subscriber("/bat", BatteryState, callback))
   
