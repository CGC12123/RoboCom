# -*- coding: UTF-8 -*-
import subprocess
import time
import os
import rospy
import tf
import yaml
import math

# 导航目标点在 home_pose.yaml 及 target_pose.yaml 中修改

# 打开导航软件
def StartNavigation():
	sh1s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start1.sh",
			"/home/robuster/RoboCom/navigation/bash/Start1.sh"]
	sh1 = "bash -c '{}'".format("; ".join(sh1s))
	subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh1, '--hold'], 
					stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	time.sleep(15) # 等待导航程序启动完成

	# 发布目标地点话题
	sh2s = ["echo 123456 | sudo -S chmod +x /home/robuster/RoboCom/navigation/bash/Start2.sh",
			"/home/robuster/RoboCom/navigation/bash/Start2.sh"]
	sh2 = "bash -c '{}'".format("; ".join(sh2s))
	subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh2, '--hold'], 
					stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	

def autoGrab():
	# 运行下一步自动夹取
	sh3s = ["python /home/robuster/RoboCom/beetle_ai/scripts/grab_right.py"]
	sh3 = "bash -c '{}'".format("; ".join(sh3s))
	subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', sh3, '--hold'], 
					stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == '__main__':
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
			rospy.loginfo("Translation: x = %f, y = %f, z = %f,   Rotation:    x = %f, y = %f, z = %f, w = %f",
				trans[0], trans[1], trans[2], rot[0], rot[1], rot[2], rot[3])
			if ((math.fabs(pose_x - trans[0]) < bias_navi) and (math.fabs(pose_y - trans[1]) < bias_navi) and (math.fabs(pose_z - trans[2]) < bias_navi)
					and (math.fabs(orien_x - rot[0]) < bias_navi) and (math.fabs(orien_y - rot[1]) < bias_navi) 
					and (math.fabs(orien_z - rot[2]) < bias_navi) and (math.fabs(orien_w - rot[3]) < bias_navi)):
				print("arrive") # 到达位置
				break
		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			continue

		rate.sleep()

	# autoGrab() # 判定到达位置后开始夹取
	