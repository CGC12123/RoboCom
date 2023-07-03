#!/bin/bash
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