import rospy
import numpy as np
import cv2 as cv
import time
import geometry_msgs.msg
import sensor_msgs.msg
from cv_bridge import CvBridge


class camera:
    def __init__(self):
        rospy.Subscriber("/camera/color/image_raw", sensor_msgs.msg.Image, self.callback_photo, queue_size=1)
    
    def callback_photo(self,msg):
        self.img = CvBridge().imgmsg_to_cv2(msg, "bgr8")
          
    def getpic(self):
        rospy.sleep(rospy.rostime.Duration(2))
        return self.img
        
        
     
        


