# Robocom
> 基于RB280

## 机械臂调整
```bash
# 打开可视化操作程序
cd ~/catkin_ws/src/mycobot_tools/myblockly
./myblockly
```

## 地图建图及导航
```bash
# 启动建图程序
roslaunch robuster_mr_navigation mapping.launch

# 打开另一个终端 停止接收传感器数据
rosservice call /finish_trajectory 0
# 储存地图
rosservice call /write_state "{filename: '${HOME}/Downloads/mymap.pbstream'}"
# 转换地图格式
rosrun cartographer_ros cartographer_pbstream_to_ros_map -map_filestem={HOME}/Downloads/mymap -pbstream_filename=/home/robuster/Downloads/mymap.pbstream -resolution=0.05

# 启动导航软件
roslaunch robuster_mr_navigation navigation.launch

# 获取设备当前坐标
rosrun tf tf_echo /map/base_link

# 导航到目标点
rostopic pub/move_base_simple/goal gemetry_msgs/PoseStaed "header:
  seq:0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: 'map'
pose:
  position:
    x:
    y: 
    z: 0.0
  orentation:
    x: 0.0
    y: 0.0
    z: 
    w:   "
```
> 下方的pose为目标导航点坐标
