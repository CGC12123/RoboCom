#!/bin/bash
rostopic pub /move_base_simple/goal geometry_msgs/PoseStamped -f target_pose.yaml