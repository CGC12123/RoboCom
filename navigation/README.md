# 导航部分
## 程序介绍
### 导航至目标点及返回出发点
```bash
# 导航至目标点
python navigation/StartNavigation.py
# 返回出发点
python navigation/BackNavigation.py
```
### 导航点设置
> 修改目标导航点在 `navigation/target_pose.yaml` 及 `navigation/home_pose.yaml` 中进行

> 主要修改参数如下
> ```
> pose:
>  position: 
>    x: 0.743
>    y: -0.208
>    z: 0.0
>  orientation: 
>    x: 0.0
>    y: 0.0
>    z: -0.034
>    w: 0.999"
> ```
> 导航点获取可查看[地图建图及导航](###地图建图及导航)

## 建图及导航使用方法
### 地图建图及导航
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
rosrun tf tf_echo /map /base_link

# 导航到目标点
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped "header:
  seq: 0
  stamp: 
    secs: 0
    nsecs: 0
  frame_id: 'map'
pose:
  position: 
    x: 0.743
    y: -0.208
    z: 0.0
  orientation: 
    x: 0.0
    y: 0.0
    z: -0.034
    w: 0.999"
```
> 下方的pose为目标导航点坐标
