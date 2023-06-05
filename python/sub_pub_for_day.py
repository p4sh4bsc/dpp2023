import rospy
from std_msgs.msg import String

pub = rospy.Publisher('chatter', String, queue_size=10)
rospy.init_node('pub')
r = rospy.Rate(10)
message = str(input("insert text: "))



while not rospy.is_shutdown():
    if message != "":
        pub.publish(message)
        message = ""
        r.sleep()
    else:
        message = str(input("insert text: "))
