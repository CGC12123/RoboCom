#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/String.h> 
#include <sensor_msgs/Joy.h>
#include <actionlib/server/simple_action_server.h>
#include <boost/shared_ptr.hpp>
#include <nav_msgs/Odometry.h>
#include <unistd.h> 

/*

	make指令：（在桌面terminal下输入）
	cd ~/mr300_ws && catkin_make -j4
	
*/

using namespace std;
 
class LogTeleop
{
public:
    LogTeleop();
 
private:
    /* data */
    void LogCallback(const sensor_msgs::Joy::ConstPtr& Joy);
    ros::NodeHandle n;
    ros::Subscriber sub ;
    ros::Publisher pub ;
    ros::Publisher cancel_pub_;
    double vlinear,vangular;
    int axis_ang_z,axis_lin_x,ton;
    actionlib_msgs::GoalID empty_goal_;
    double acc_linear_x;
    double current_linear_x;
    bool b_flag;
};
 
LogTeleop::LogTeleop()
{
    n.param<int>("axis_linear_x",axis_lin_x,1);
    n.param<int>("axis_angular_z",axis_ang_z,2);
    n.param<double>("vel_linear",vlinear,0.25);
    n.param<double>("vel_angular",vangular,0.2);
    n.param<int>("button",ton,5);
    n.param<double>("acc_linear_x",acc_linear_x,0.1);
    pub= n.advertise<geometry_msgs::Twist>("cmd_vel", 1, true);
    sub = n.subscribe<sensor_msgs::Joy>("joy",1,&LogTeleop::LogCallback,this);
    cancel_pub_ = n.advertise<actionlib_msgs::GoalID>("move_base/cancel",1);
    b_flag = false;
}


void LogTeleop::LogCallback(const sensor_msgs::Joy::ConstPtr& Joy)
{
	geometry_msgs::Twist twist;

	if(Joy->buttons[ton])//button RB
	{
		if(Joy->buttons[3])//button Y
		{
			system("killall -9 python");
			if(Joy->buttons[4])//button LB
			{
				system("python /home/robuster/beetle_ai/scripts/high.py");
				printf("high");
			}
			else
			{
				system("python /home/robuster/beetle_ai/scripts/grab_high.py");
				printf("grab_high");
			}			 
			ros::Duration(1).sleep();
		}
		else if(Joy->buttons[1])//button A
		{
			system("killall -9  python");
			if(Joy->buttons[4])//button LB
			{
				system("python /home/robuster/beetle_ai/scripts/low.py");
				printf("low");
			}
			else
			{
				system("python /home/robuster/beetle_ai/scripts/grab_low.py");
				printf("grab_low");
			}			  
			ros::Duration(1).sleep();
		}
		else if(Joy->buttons[0])
		{
			system("killall -9  python");
			printf("kill"); 
			ros::Duration(1).sleep();
		}
		else if(Joy->buttons[2])
		{
			system("killall -9  python");
			system("python /home/robuster/beetle_ai/scripts/down.py");
			printf("down"); 
			ros::Duration(1).sleep();
		}
		else if(Joy->buttons[8])//button Back
		{
			system("killall -9  python");
			system("python /home/robuster/beetle_ai/scripts/home.py");
			printf("home"); 
			ros::Duration(1).sleep();
		}
		else if(Joy->buttons[9])//button Start
		{
			system("killall -9  python");
			system("python /home/robuster/beetle_ai/scripts/zero.py");
			printf("zero"); 
			ros::Duration(1).sleep();
		}

		b_flag = true;

		vlinear = vlinear * (1 + (Joy->axes[5] * 0.1));
		if(vlinear>=1.0)
		   vlinear = 1.0;
		else if (vlinear<=0.1)
		   vlinear = 0.1;
		else
		   vlinear = vlinear;
		
		vangular = vangular * (1 +  (Joy->axes[4] * 0.1));
		if(vangular>=1.5)
			vangular = 1.5;
		else if(vangular<=0.1)
			vangular = 0.1;
		else
			vangular = vangular;

	    twist.linear.x =(Joy->axes[axis_lin_x])*vlinear;
	    twist.linear.y = 0;
	    twist.linear.z = 0;
	    
	    twist.angular.x = 0;
	    twist.angular.y = 0;
	    twist.angular.z =(Joy->axes[axis_ang_z])*vangular;

		pub.publish(twist);

		cancel_pub_.publish(empty_goal_);
	}
	else
	{
		if(b_flag)
		{
			twist.linear.x = 0;
		    twist.linear.y = 0;
		    twist.linear.z = 0;
		    
		    twist.angular.x = 0;
		    twist.angular.y = 0;
		    twist.angular.z = 0;
			pub.publish(twist);
			b_flag = false;
		}
	}

	

}

int main(int argc,char** argv)
{
    ros::init(argc, argv, "logitech_teleop_node");    
    LogTeleop  logteleop;
    ros::spin();
    return 0;
}

