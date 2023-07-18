#encoding: UTF-8
#!/usr/bin/env python2

class GrabParams(object):
#基本参数
	y_bias = 5
	x_bias = 40
	debug = True #True         
	ONNX_MODEL = '/home/robuster/beetle_ai/scripts/beetle_obj.onnx'
	IMG_SIZE = 128 # 尽量不要动 有未知bug还没解决
	done = False
	usb_dev = "/dev/arm" 
	baudrate = 115200

	#                   [x   y    z   俯仰  横滚  航向 ]	
	coords_high_right = [94, -63, 310, -80, 45, -90]
	coords_high_left  = [94,  63, 310, -85, 45, -85]

	coords_low_right  = [176, -61, 225, -75, 45, -83]
	coords_low_left   = [176,  61, 225, -78, 57, -85]

	# 仓库货架使用
	coords_right_high = [-50.7, -130.1, 285.6, -85.45, 54.12, -173.88] # 向右高初始状态
	# coords_right_low  = [-54.9, -140.4, 214.0, -90.25, 47.02, -175.88] # 向右低初始状态
	coords_right_low  = [-50.6, -122.3, 225.0, -100.39, 43.41, 169.96] # 向右低初始状态

	# 公共区使用
	coords_left_high  = [53.7, 112.0, 318.0, -85.93, 52.13, 7.59] # 向左高初始状态
	coords_left_low   = [53.7, 112.0, 220.0, -85.93, 52.13, 7.59] # 向左低初始状态

	# 充能站使用
	coords_under      = [51.8, 170.7, 240, -179.16, 11.07, -45.73] # 向下初始状态
	# coords_under      = [51.8, 170.7 + 40, 240 - 80, -179.16, 11.07, -45.73] # 向下初始状态

	# 放置入库位置 #
	# 1234为向右夹取时的参数 5678为向左
	coords_pitchdown1 	= [-59.5, -33.5, 392.3, -89.36, 46.69, -168.89] # 使其先抬高 避免碰撞
	coords_pitchdown2 	= [-173.4, -34.3, 235.5, 174.35, -5.38, 71.52] # 入库

	coords_pitchdown3 	= [-104.6, -87.3, 249.0, -101.26, 41.03, 135.54] # 使其撤出来 避免碰撞
	coords_pitchdown4 	= [-173.4, -34.3, 230.5, 174.35, -5.38, 71.52] # 入库

	coords_pitchdown5 	= [106.9, 94.9, 368.9, -95.48, 54.7, -25.65] # 使其先抬高 避免碰撞 左侧夹取时使用 为较高的架子 可调可不调
	coords_pitchdown6 	= [-180.4, -10.3, 235.5, 195.35, -5.38, 71.52] # 入库

	coords_pitchdown7 	= [12.6, 156.9, 248.6, -93.1, 50.42, 2.12] # 使其撤出来 避免碰撞
	coords_pitchdown8 	= [-214.0, -11.7, 194.1, 179.95, -0.66, 47.19]	 # 入库

	coords_pitchdown9 	= [14.5, -128.5, 316.0, -138.53, 19.09, -163.97] # 使其撤出来 避免碰撞
	coords_pitchdown10	= [-173.1, 18.6, 218.0, -173.95, -0.37, 65.74] # 入库 充能站使用


#需要调试的参数
	cap_num = 2   # 摄像头编号
	cap_num2 = 3   # 摄像头编号2 备用 有时1会死掉

	ratio       = 0.8 	# 画面中坐标换算为实际前进坐标的值
	ratio_color = -0.8 	# 颜色夹取中画面中坐标换算为实际前进坐标的值

	dist_bias 	= 1 	# 前近距离与预估值的比例 设定为100cm其大约前进92cm 可细调

	bias_right_high_x = 0 	# 向右边夹取时 夹取前后的左右变化 左+右-
	bias_right_high_y = -70 # 向右边夹取时 夹取前后的前后变化 前-后+
	bias_right_high_z = 55 	# 向右边夹取时 夹取前后的高度变化 高+低-

	bias_right_low_x = 0 	# 向右边夹取时 夹取前后的左右变化 左+右-
	bias_right_low_y = -55  # 向右边夹取时 夹取前后的前后变化 前-后+
	bias_right_low_z = 45 	# 向右边夹取时 夹取前后的高度变化 高+低-

	bias_left_high_x = 0 	# 向左边夹取时 夹取前后的左右变化 左+右-
	bias_left_high_y = 55   # 向左边夹取时 夹取前后的前后变化 前+后-
	bias_left_high_z = 40 	# 向左边夹取时 夹取前后的高度变化 高+低-

	bias_left_low_x = 0 	# 向左边夹取时 夹取前后的左右变化 左+右-
	bias_left_low_y = 70   	# 向左边夹取时 夹取前后的前后变化 前+后-
	bias_left_low_z = 35 	# 向左边夹取时 夹取前后的高度变化 高+低-

	bias_under_x = 0 		# 向下夹取时 夹取前后的左右变化 左-右+
	bias_under_y = 50    	# 向下夹取时 夹取前后的前后变化 前+后- 为了弥补摄像头和夹爪的位置差
	bias_under_z = -80 		# 向下夹取时 夹取前后的高度变化 高+低-

#物块放置测距误差，基本不用动
	set_diff = 0

#判断识别物是否是目标，  对应数字，改detect_target
	classes = ("apple", "clock", "banana","cat ","bird ")
	#             0       1       2      3        4
	detect_target = 0

# 目标颜色修改
	colors = ['red', 'green', 'blue', 'yellow', 'purple']
	#           0       1       2        3
	color = 2

# 字符识别修改
	characters = ['油', '粮']
	#              0     1
	character = 1




	# 以下为旧代码参数 待整理
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

grabParams = GrabParams()

