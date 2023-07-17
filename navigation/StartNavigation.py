# -*- coding: UTF-8 -*-
import subprocess
import time
import os
import rospy
import tf
import yaml
import math
import signal
import actionlib
import threading
from actionlib_msgs.msg import GoalStatus
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseStamped, Pose, Point, Quaternion
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# 导航目标点在 home_pose.yaml 及 target_pose.yaml 中修改

def StartNavigation():
	with open('/home/robuster/RoboCom/navigation/target_pose.yaml', 'r') as f:
		yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

	pose_x = yaml_data['pose']['position']['x']
	pose_y = yaml_data['pose']['position']['y']
	pose_z = yaml_data['pose']['position']['z']

	orien_x = yaml_data['pose']['orientation']['x']
	orien_y = yaml_data['pose']['orientation']['y']
	orien_z = yaml_data['pose']['orientation']['z']
	orien_w = yaml_data['pose']['orientation']['w']

	goal = MoveBaseGoal()
	goal.target_pose.pose = Pose(Point(pose_x, pose_y, pose_z),
								 Quaternion(orien_x, orien_y, orien_z, orien_w))
	global flag
	flag = 0
	send_goal(goal)
	while not flag:
		time.sleep(1)

def autoGrab():
	# 运行下一步自动夹取
	os.system("python /home/robuster/RoboCom/beetle_ai/scripts/grab_right.py")
	# sh3s = ["echo 123456 | sudo -S chmod 777 /home/robuster/RoboCom/navigation/bash/StartGrab.sh",
	# 		"/home/robuster/RoboCom/navigation/bash/StartGrab.sh"]
	# sh3 = "bash -c '{}'".format("; ".join(sh3s))
	# subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3, '--hold'], 
	# 				stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def send_goal(goal):
	client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	client.wait_for_server()
	goal.target_pose.header.frame_id = 'map'
	goal.target_pose.header.stamp = rospy.Time.now()
	client.send_goal(goal, done_cb=goal_reached_callback)
	client.wait_for_result()

def goal_reached_callback(goal_status, result):
	global flag
	if goal_status == GoalStatus.SUCCEEDED:
		print("Navigation succeeded!")
	else:
		print("Navigation failed!")
	flag = 1

def ChangePosture():
	# os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right_low.py")
	pass

if __name__ == '__main__':
	# 调整姿态
	ChangePosture()

	rospy.init_node('navigation')
	# 开始导航
	# 创建一个线程来执行 StartNavigation() 函数
	nav_thread = threading.Thread(target=StartNavigation)
	nav_thread.start()
	# 等待导航线程结束
	nav_thread.join()
	# StartNavigation()
	print(1)
	time.sleep(3)
	autoGrab() # 判定到达位置后开始夹取
	