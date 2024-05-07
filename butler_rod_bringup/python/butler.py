#!/usr/bin/env python3
import copy
import rospy
import roslaunch
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
import numpy as np
import sys
import math
import time
from transform import transformer

class butler:

    def __init__(self,nodename="butler",groupname="manipulator"):
        rospy.init_node(nodename, anonymous=False)
        time.sleep(0.1)
        moveit_commander.roscpp_initialize(sys.argv)
        time.sleep(0.1)
        self.robot = moveit_commander.RobotCommander()
        time.sleep(0.1)
        self.move_group = moveit_commander.MoveGroupCommander(groupname)
        time.sleep(0.1)
        
        #Acceleration and Speed factors
        self.move_group.set_max_acceleration_scaling_factor(1)
        self.move_group.set_max_velocity_scaling_factor(1)
        
        self.move_group.set_goal_tolerance(0.001) #For real robot set the tolerance to 1 mm
        self.move_group.set_pose_reference_frame("base_link") 		
        self.goals = []
        self.t = transformer()
        
    def __del__(self):
        self.move_group.stop()
        print("Stopping")         

    def info(self,show=False):
        self.cp = self.move_group.get_current_pose()
        #self.cp = self.t.toBase(self.cp)
        #self.cp = self.cp.pose
        
        if show:
            #print("Info: current pose in base_link")
            #print("x: ",self.cp.position.x)
            #print("y: ",self.cp.position.y)
            #print("z: ",self.cp.position.z)
            print(self.cp)
            quat = (self.cp.pose.orientation.x, self.cp.pose.orientation.y, self.cp.pose.orientation.z, self.cp.pose.orientation.w)
            rpy = tf.transformations.euler_from_quaternion(quat)
            print("ROLL/PITCH/YAW:")
            print("roll: ",rpy[0])
            print("pitch: ",rpy[1])
            print("yaw: ",rpy[2])
            #print("qx: ",self.cp.orientation.x)
            #print("qy: ",self.cp.orientation.y)
            #print("qz: ",self.cp.orientation.z)
            #print("qw: ",self.cp.orientation.w)
        return self.cp
        
        
    def setGoal(self,goal):
        try:
            self.goals.append(copy.deepcopy(goal))
        except:
            print("Ziel konnte nicht gesetzt werden")
        
    def setTarget(self,x,y,z,roll,pitch,yaw):
        goal = geometry_msgs.msg.Pose()

        qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
        qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
        qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
        qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)

        goal.position.x = x
        goal.position.y = y
        goal.position.z = z
        goal.orientation.x = qx
        goal.orientation.y = qy
        goal.orientation.z = qz
        goal.orientation.w = qw

        try:
            self.goals.append(copy.deepcopy(goal))
    
        except:
            print("Target not set")

    def move(self):

        self.move_group.clear_pose_targets()
        try:
            for g in self.goals:
                self.move_group.set_pose_target(g)
                self.move_group.go(wait=True)
        except:
            print("Targets not reachable")
        finally:
            print("Move Command finished")
            self.move_group.stop()
            self.move_group.clear_pose_targets()
            self.goals = []
