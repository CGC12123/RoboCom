# -*- coding: UTF-8 -*-
import subprocess
import time
import os
import signal
import actionlib
import rospy
import yaml
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# 回到出发点
def send_home(goal):
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	client.send_goal(goal)  #, done_cb=home_reached_callback

if __name__ == '__main__':
	with open('/home/robuster/RoboCom/navigation/home_pose.yaml', 'r') as f:
		yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

	pose_x = yaml_data['pose']['position']['x']
	pose_y = yaml_data['pose']['position']['y']
	pose_z = yaml_data['pose']['position']['z']

	orien_x = yaml_data['pose']['orientation']['x']
	orien_y = yaml_data['pose']['orientation']['y']
	orien_z = yaml_data['pose']['orientation']['z']
	orien_w = yaml_data['pose']['orientation']['w']

	home = MoveBaseGoal()
	home.target_pose.pose = Pose(Point(pose_x, pose_y, pose_z),
								 Quaternion(orien_x, orien_y, orien_z, orien_w))
	send_home(home)