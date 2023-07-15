#!/bin/bash
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped -f /home/robuster/RoboCom/navigation/target_pose.yaml