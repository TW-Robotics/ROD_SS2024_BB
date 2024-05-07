#!/usr/bin/env python3
from cameranew import camera
from butler import butler
from transform import transformer
import geometry_msgs.msg
import cv2 as cv
from cylinderDetect import CylinderDedecter
from def_state_gripper import gripper
import time



if __name__ == "__main__":

    #Initialize Robot(Planning group = manipulator for UR5 real robot) and Gripper (is connected via /dev/ttyUSB0 with the PC)
    r = butler(nodename="ur5",groupname="manipulator")
    t = transformer() 
    c = camera()
    d = CylinderDedecter()
    g = gripper() 
    w = 1280
    h = 720
    cx = 653.15
    cy = 387.62
    fx = 909.86
    fy = 909.08
    
    while True:
        #Print current pose
        #r.info() --> return current poseStamped
        g.open_gripper()
        img = c.getpic()
        cv.imshow("Window",img)
        cv.waitKey(1000)
        cord = d.calculateCenter(img)
        print(cord)
        r.info(show=True)
        x_3d = ((cord[0] - cx) * 0.5)/fx
        y_3d = ((cord[1] - cy) * 0.5)/fy
        
        #Example Camera Pose
        camera_pose = geometry_msgs.msg.PoseStamped()
        camera_pose.header.frame_id = "camera_color_optical_frame"
        camera_pose.pose.position.x = x_3d
        camera_pose.pose.position.y = y_3d
        camera_pose.pose.position.z = 0.55
        camera_pose.pose.orientation.x = 0.0
        camera_pose.pose.orientation.y = 0.0
        camera_pose.pose.orientation.z = 0.0
        camera_pose.pose.orientation.w = 1.0
        
        #Example home Pose
        #home_pos = geometry_msgs.msg.PoseStamped()
        #home_pos.header.frame_id = "base_link"
        #home_pos.pose.position.x = 0.4871
        #home_pos.pose.position.y = 0.1106
        #home_pos.pose.position.z = 0.4274
        #home_pos.pose.orientation.x = -0.707
        #home_pos.pose.orientation.y = 0.707
        #home_pos.pose.orientation.z = 0.0
        #home_pos.pose.orientation.w = 0.0

        #Transformation Camera to base_link frame
        camera_in_base = t.toBase(camera_pose)
        
        
        #Set Goal Pose Stamped
        r.setTarget(0.4871,0.1106,0.4274, -3.14,0,-1.57)
        r.setGoal(camera_in_base)
        

        #Set target
        #r.setTarget(x,y,z, r,p,y): eg. r.setTarget(0.55,-0.25,0, -3.14,0,-1.57)
        
        #Move the robot
        r.move()
        g.close_gripper()
        r.setTarget(0.4871,0.1106,0.4274, -3.14,0,-1.57)
        r.move()
        g.open_gripper()
        time.sleep(5)
    
    
    #Open and Close Gripper
    #Open: rostopic pub /gripper_open std_msgs/Bool "data: true"
    #Close: rostopic pub /gripper_open std_msgs/Bool "data: false"
    


    

    
    #delete robot and transformer object
    del r
    del t
