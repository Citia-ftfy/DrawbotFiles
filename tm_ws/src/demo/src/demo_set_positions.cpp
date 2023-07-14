// ROS headers
#include <ros/ros.h>
#include <std_msgs/String.h>

// std header
#include <sstream>
#include <cstdlib>

// TM Driver header
#include "tm_msgs/SetPositions.h"

int main(int argc, char **argv)
{  
  ros::init(argc, argv, "demo_set_positions");      
  ros::NodeHandle nh_demo; 
  ros::ServiceClient client = nh_demo.serviceClient<tm_msgs::SetPositions>("tm_driver/set_positions");
  tm_msgs::SetPositions srv;
  
  
  double	j1 = 1.58, //shoulder turn
            j2 = 0.1, //shoulder bend
            j3 = 1.58, //elbow 
            j4 = 0, // wrist1
            j5 = 1.58, // wrist2
            j6 = 0, // wrist 3
			velocity = 0.4, // in rad/s
			acc_time = 0.2;
  
  
  if(argc >= 1+6) { // cmd name + args
        j1 = std::atof(argv[1]);
        j2 = std::atof(argv[2]);
        j3 = std::atof(argv[3]);
        j4 = std::atof(argv[4]);
        j5 = std::atof(argv[5]);
        j6 = std::atof(argv[6]);
		
		if(argc == 8){
			velocity = std::atof(argv[7]);
		}
		if(argc == 9){
			acc_time = std::atof(argv[8]);
		}
   }
   
  	
  //Request
  srv.request.motion_type = tm_msgs::SetPositions::Request::PTP_J;
  srv.request.positions.push_back(j1);
  srv.request.positions.push_back(j2);
  srv.request.positions.push_back(j3);
  srv.request.positions.push_back(j4);
  srv.request.positions.push_back(j5);
  srv.request.positions.push_back(j6);
  srv.request.velocity = velocity;//rad/s
  srv.request.acc_time = acc_time;
  srv.request.blend_percentage = 10;
  srv.request.fine_goal  = false;

  if (client.call(srv))                             
  {
    if (srv.response.ok) ROS_INFO_STREAM("SetPositions to robot");
    else ROS_WARN_STREAM("SetPositions to robot , but response not yet ok ");
  }
  else
  {
    ROS_ERROR_STREAM("Error SetPositions to robot");
    return 1;
  }

  //ROS_INFO_STREAM_NAMED("SetPositions", "shutdown.");  	
  return 0;
}
