import rospy
from std_msgs.msg import Bool
import std_msgs.msg
import time

class gripper():
    def __init__(self):
        #rospy.init_node("gripper_state", anonymous = True)
        self.pub = rospy.Publisher("/gripper_open", Bool, queue_size=10)
        
    def open_gripper(self):
        open_grip = std_msgs.msg.Bool
        open_grip = True
        for i in range(1, 10):
            self.pub.publish(open_grip)
            time.sleep(0.1)
            
        
        
    def close_gripper(self):
        close_grip = std_msgs.msg.Bool
        close_grip = False
        self.pub.publish(close_grip)
        for i in range(1, 10):
            self.pub.publish(close_grip)
            time.sleep(0.1)



