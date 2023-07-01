#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):
#基本参数
	#                   [x   y    z   俯仰  横滚  航向 ]	
	coords_high_right = [94, -63, 310, -80, 45, -90]
	coords_high_left  = [94,  63, 310, -85, 45, -85]

	coords_low_right  = [176, -61, 225, -75, 45, -83]
	coords_low_left   = [176,  61, 225, -78, 57, -85]

	# 仓库货架使用
	coords_right_high 		= [-50.7, -120.1, 290.6, -85.45, 46.39, -173.88] # 向右高初始状态
	coords_right_low  		= [] # 向右低初始状态

	# 充能站使用
	coords_down       = [] # 向下初始状态

	# 放置入库位置
	coords_pitchdown1  = [-59.5, -33.5, 392.3, -89.36, 46.69, -168.89] # 使其先抬高 避免碰撞
	coords_pitchdown2  = [-173.4, -34.3, 235.5, 174.35, -5.38, 71.52] # 入库

	y_bias = 5
	x_bias = 40
	debug = True #True         
	ONNX_MODEL = '/home/robuster/beetle_ai/scripts/beetle_obj.onnx'
	IMG_SIZE = 128
	done = False
	usb_dev = "/dev/arm" 
	baudrate = 115200

#需要调试的参数
	cap_num = 2   #摄像头编号

	ratio = 0.8 # 画面中坐标换算为实际前进坐标的值

	bias_right_high_x = 0 	# 向右边夹取时 夹取前后的左右变化 左+右-
	bias_right_high_y = -80   # 向右边夹取时 夹取前后的前后变化 前-后+
	bias_right_high_z = 35 	# 向右边夹取时 夹取前后的高度变化 高+低-

	# 以下为旧代码
	put_down_direction = "left"#放置方向，位于车左还是右
	grab_low_right    =	287     #低左   的机械臂高度      加+高   减-低  以5为单位调节   
	grab_low_left     = 277     #低右   的机械臂高度      同上
	grab_high_right   = 355     #高右   的机械臂高度  
	grab_high_left    = 347		#高左   的机械臂高度  

	grab_right_high   = 0 		# 向右时机械臂的高度
	grab_right_low    = 0 		# 向右时机械臂的高度

	grab_down         = 0  		# 向下时的机械臂高度
#夹取机械臂俯仰角调节
	pitch_low_right    = 10     #低左   的机械臂高度      加+向上   减-向下  以2左右为单位调节   
	pitch_low_left     = 7      #低右   的机械臂高度      同上
	pitch_high_right   = 7      #高右   的机械臂高度  
	pitch_high_left    = 7		#高左   的机械臂高度  

	pitch_down		   = 0 		# 向下
#夹取机械臂横滚角调节
	roll_low_right    = -5      #低左   的机械臂高度      加+向右   减-向左  以2左右为单位调节   
	roll_low_left     = 0       #低右   的机械臂高度      同上
	roll_high_right   = -5      #高右   的机械臂高度  
	roll_high_left    = 5		#高左   的机械臂高度 

	roll_down	      = 0 		# 向下


#测距误差抵消     +x 多前进x cm ， -x 少前进x cm 
	move_power_high_right  = 2.5       #高右
	move_power_high_left   = 2.5     #高左
	move_power_low_right   = -1    #低右
	move_power_low_left    = 2    #低左

#物块放置测距误差，基本不用动
	set_diff = 0
#判断识别物是否是目标，  对应数字，改detect_target
	classes = ("apple", "clock", "banana","cat ","bird ")
	#             0       1       2      3        4
	detect_target = 0

# 目标颜色修改
	colors = ['red', 'green', 'bule', 'yellow']
	#           0       1       2        3
	color = colors[0]

# 字符识别修改
	characters = ['油', '粮']
	#              0     1
	character = characters[0]

grabParams = GrabParams()

