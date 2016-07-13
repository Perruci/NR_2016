#!/usr/bin/env python

from std_msgs.msg import Float64MultiArray
import termios, fcntl, sys, os
import rospy

#import service library
from std_srvs.srv import Empty

#topic to command
thrusters_topic = "/g500/thrusters_input"
#base velocity for the teleoperation (0.5 m/s) / (0.5rad/s)
baseBoost = 0.5

#Console input variables to teleop it from the console
fd = sys.stdin.fileno()
oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)
oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

##create the publisher
pub = rospy.Publisher(thrusters_topic, Float64MultiArray, queue_size=1)
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
    	Dynamics = [0,0,0,0,0]	
    	msg = Float64MultiArray()
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
	    ## Linear Acelerations 
	    ### w_s x-axis
	    elif c=='w':  
		Dynamics[0] = Dynamics[1] = -baseBoost
	    elif c=='s':
		Dynamics[0] = Dynamics[1] = baseBoost
	    ### a_d y-axis
	    elif c=='a':	
		Dynamics[2] = Dynamics[3] = baseBoost
	    elif c=='d':	
		Dynamics[2] = Dynamics[3] = -baseBoost
	    ### q_e z-axis
	    elif c=='q':	
		Dynamics[4] = baseBoost
	    elif c=='e':	
		Dynamics[4] = -baseBoost
	    
	    else:
		print 'wrong key pressed'
	    while c!='':
	        c = sys.stdin.read(1)
        except IOError: pass

        ##publish the message
        msg.data = Dynamics
	pub.publish(msg)
	rospy.sleep(0.1)

##Other input stuff
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
