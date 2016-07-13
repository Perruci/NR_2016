#!/usr/bin/env python

from geometry_msgs.msg import TwistStamped
import termios, fcntl, sys, os
import rospy

#import service library
from std_srvs.srv import Empty

#topic to command
twist_topic="/g500/velocityCommand"
#base velocity for the teleoperation (0.5 m/s) / (0.5rad/s)
baseVelocity=0.5

#Console input variables to teleop it from the console
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

##create the publisher
pub = rospy.Publisher(twist_topic, TwistStamped,queue_size=1)
rospy.init_node('keyboardCommand')

##wait for benchmark init service
rospy.wait_for_service('/startBench')
start=rospy.ServiceProxy('/startBench', Empty)

##wait for benchmark stop service
rospy.wait_for_service('/stopBench')
stop=rospy.ServiceProxy('/stopBench', Empty)

#The try is necessary for the console input!
try:
    while not rospy.is_shutdown():
	msg = TwistStamped()
        try:
            c = sys.stdin.read(1)
	    ## Set Benchmarking
	    if c=='\n':
		start()
	  	print "Benchmarking Started!"
	    elif c==' ':
		stop()
		print "Benchmark finished!"	  
            
	    ## Depending on the character set the proper speeds
	    ## Linear Velocities
	    ### w_s x-axis
	    elif c=='w':  
		msg.twist.linear.x=-baseVelocity
	    elif c=='s':
		msg.twist.linear.x=baseVelocity
	    ### a_d y-axis
	    elif c=='a':	
		msg.twist.linear.y=-baseVelocity
	    elif c=='d':	
		msg.twist.linear.y=baseVelocity
	    ### q_e z-axis
	    elif c=='q':	
		msg.twist.linear.z=-baseVelocity
	    elif c=='e':	
		msg.twist.linear.z=baseVelocity
	    ## Angular Velocities
	    ### i_k x-axis
	    elif c=='i':  
		msg.twist.angular.x=-baseVelocity
	    elif c=='k':
		msg.twist.angular.x=baseVelocity
	    ### j_l y-axis
	    elif c=='j':	
		msg.twist.angular.y=-baseVelocity
	    elif c=='l':	
		msg.twist.angular.y=baseVelocity
	    ### u_o z-axis
	    elif c=='u':	
		msg.twist.angular.z=-baseVelocity
	    elif c=='o':	
		msg.twist.angular.z=baseVelocity
	    
	    else:
		print 'wrong key pressed'
	    while c!='':
	        c = sys.stdin.read(1)
        except IOError: pass

        ##publish the message
        pub.publish(msg)
	rospy.sleep(0.1)

##Other input stuff
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
