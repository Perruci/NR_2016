### Synthesis of Principal Commands

* Add new files to the workspace

	src/CmakeLists.txt on each directory

* Compile your files

	catkin_make install

* Create multiple Terminal windows

1 -  Set up ROS environment

	roscore

2.0 - Basic Simulation

	rosrun uwsim uwsim - -configfile pipeFollowing_basic.xml
	rosrun uwsim uwsim - -configfile pipeFollowing_turns.xml
	rosrun uwsim uwsim - -configfile pipeFollowing_heights.xml

2.1 - Lauch Simulation

	roslaunch pipefollowing basic.launch
	roslaunch pipefollowing turns.launch
	roslaunch pipefollowing heights.launch

3 - Run your programs

	rosrun pipefollowing PF_teleop.py

