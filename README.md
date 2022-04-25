# CS499INCLUDE
INCLUDE Husky UGV simulation with cv and movement functionality

IMPORTANT NOTE:
-Must be run on Ubuntu or it will not work

Install Instructions:
-clone the repo
-Follow this guide to install ROS2
  -https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html
-Follow this guide to setup the workspace and get dependencies
  -https://docs.ros.org/en/foxy/Tutorials/Workspace/Creating-A-Workspace.html
   -check prerequisite installations for this tutorial
-Make sure the packages have been built using the "colcon build" command (while in the workspace directory)
-open 3 terminal windows
  -in the first window make sure to be in your workspace directory and run
    ros2 launch basic_mobile_robot basic_mobile_bot_v2.launch.py
  -in the second windoww make sure to be in your workspace directory and run
    ros2 run cv_basics img_subscriber
  -in the third window run 
    rqt_robot_steering
