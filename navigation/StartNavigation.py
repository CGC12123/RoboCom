# -*- coding: UTF-8 -*-
import subprocess
import time
import os
import rospy
import tf
import yaml
import math
import signal

# 导航目标点在 home_pose.yaml 及 target_pose.yaml 中修改

def StartNavigation():
	# 打开导航软件
	sh1s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start1.sh",
			"/home/robuster/RoboCom/navigation/bash/Start1.sh"]
	sh1 = "bash -c '{}'".format("; ".join(sh1s))
	subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
					stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	time.sleep(15) # 等待导航程序启动完成

	# 发布目标地点话题
	sh2s = ["/home/robuster/RoboCom/navigation/bash/Start2.sh"]
	sh2 = "bash -c '{}'".format("; ".join(sh2s))
	process = subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
					stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	time.sleep(8)
	process.kill()
	# pid = process.pid
	# # 打开文件，如果不存在则创建
	# with open('/home/robuster/RoboCom/navigation/pid.txt', 'w') as file:
	# 	# 写入内容
	# 	file.write(pid)

def autoGrab():
	# 运行下一步自动夹取
	os.system("/home/robuster/RoboCom/navigation/bash/StartGrab.sh")
	# sh3s = ["echo 123456 | sudo -S chmod 777 /home/robuster/RoboCom/navigation/bash/StartGrab.sh",
	# 		"/home/robuster/RoboCom/navigation/bash/StartGrab.sh"]
	# sh3 = "bash -c '{}'".format("; ".join(sh3s))
	# subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3, '--hold'], 
	# 				stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def killNode():
	# 关闭导航节点
	sh4s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Killnode.sh",
			"/home/robuster/RoboCom/navigation/bash/Killnode.sh"]
	sh4 = "bash -c '{}'".format("; ".join(sh4s))
	subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh4, '--hold'], 
					stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def ChangePosture():
	# os.system("python /home/robuster/RoboCom/beetle_ai/scripts/zero.py")
	# time.sleep(0.4)
	# os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right.py")
	# time.sleep(0.3)
	os.system("python /home/robuster/RoboCom/beetle_ai/scripts/right_low.py")

if __name__ == '__main__':
	# 调整姿态
	ChangePosture()

	# 开始导航
	StartNavigation()

	# 读取目标位置YAML文件中的数据
	with open('/home/robuster/RoboCom/navigation/target_pose.yaml', 'r') as f:
		yaml_data = yaml.load(f, Loader=yaml.SafeLoader)

	pose_x = yaml_data['pose']['position']['x']
	pose_y = yaml_data['pose']['position']['y']
	pose_z = yaml_data['pose']['position']['z']

	orien_x = yaml_data['pose']['orientation']['x']
	orien_y = yaml_data['pose']['orientation']['y']
	orien_z = yaml_data['pose']['orientation']['z']
	orien_w = yaml_data['pose']['orientation']['w']

	# 监听tf
	rospy.init_node('tf_listener')
	listener = tf.TransformListener()
	rate = rospy.Rate(10.0)

	# 导航点允许的误差值
	bias_navi = 0.1

	while not rospy.is_shutdown():
		try:
			(trans, rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))

			# rospy.loginfo("Translation: x = %f, y = %f, z = %f,   Rotation:    x = %f, y = %f, z = %f, w = %f",
			# 	trans[0], trans[1], trans[2], rot[0], rot[1], rot[2], rot[3])

			# if ((math.fabs(pose_x - trans[0]) < bias_navi) and (math.fabs(pose_y - trans[1]) < bias_navi) and (math.fabs(pose_z - trans[2]) < bias_navi)
			# 		and (math.fabs(orien_x - rot[0]) < bias_navi) and (math.fabs(orien_y - rot[1]) < bias_navi) 
			# 		and (math.fabs(orien_z - rot[2]) < bias_navi) and (math.fabs(orien_w - rot[3]) < bias_navi)):
			if ((math.fabs(pose_x - trans[0]) < bias_navi) and (math.fabs(pose_y - trans[1]) < bias_navi)
					and (math.fabs(orien_x - rot[0]) < bias_navi) and (math.fabs(orien_y - rot[1]) < bias_navi) 
					and (math.fabs(orien_z - rot[2]) < bias_navi) and (math.fabs(orien_w - rot[3]) < bias_navi)):
				print("arrive") # 到达位置
				killNode()
				break
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue

		rate.sleep()

	time.sleep(3)
	autoGrab() # 判定到达位置后开始夹取
	