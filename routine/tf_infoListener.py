# -*- coding: UTF-8 -*-
# 监听tf
import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('tf_listener')

    listener = tf.TransformListener()

    rate = rospy.Rate(10.0)

    while not rospy.is_shutdown():
        try:
            (trans, rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
            rospy.loginfo("Translation: x = %f, y = %f, z = %f",
                trans[0], trans[1], trans[2])
            rospy.loginfo("Rotation:    x = %f, y = %f, z = %f, w = %f",
                rot[0], rot[1], rot[2], rot[3])
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        rate.sleep()