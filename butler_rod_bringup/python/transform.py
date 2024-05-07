#!/usr/bin/env python3
import rospy
import tf
import geometry_msgs.msg
import time
import numpy as np

class transformer:
    def __init__(self):
        self.listener = tf.TransformListener()
        time.sleep(0.1)
                         
    def toBase(self,camera_pose):
        
        self.listener.waitForTransform("base_link", camera_pose.header.frame_id, rospy.Time(), rospy.Duration(4.0))

        camera_trans = (camera_pose.pose.position.x, camera_pose.pose.position.y, camera_pose.pose.position.z)
        camera_rot = (camera_pose.pose.orientation.x, camera_pose.pose.orientation.y,
                      camera_pose.pose.orientation.z, camera_pose.pose.orientation.w)

        try:
            (trans, rot) = self.listener.lookupTransform('base_link', camera_pose.header.frame_id, rospy.Time(0))
            T_base_cam = tf.transformations.compose_matrix(translate=trans, angles=tf.transformations.euler_from_quaternion(rot))
            camera_T = tf.transformations.translation_matrix(camera_trans)
            camera_R = tf.transformations.quaternion_matrix(camera_rot)
            camera_pose_matrix = np.dot(camera_T, camera_R)
            base_pose_matrix = np.dot(T_base_cam, camera_pose_matrix)
            
            # Convert the base_pose_matrix back to PoseStamped message
            base_pose = geometry_msgs.msg.PoseStamped()
            base_pose.header.frame_id = "base_link"
            (base_pose.pose.position.x, base_pose.pose.position.y, base_pose.pose.position.z) = tf.transformations.translation_from_matrix(base_pose_matrix)
            (base_pose.pose.orientation.x, base_pose.pose.orientation.y, base_pose.pose.orientation.z, base_pose.pose.orientation.w) = tf.transformations.quaternion_from_matrix(base_pose_matrix)
            
            return base_pose
        except:
            print("Transformation of pose to base_link failed!")
            return None




