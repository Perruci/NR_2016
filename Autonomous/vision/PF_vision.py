#!/usr/bin/env python

from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import Image
import rospy
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

#import service library
from std_srvs.srv import Empty

##Return the medium line detected
def get_mediumLine( lines ):
  iterator = 0
  med_x1 = 0
  med_y1 = 0
  med_x2 = 0
  med_y2 = 0
  if lines != None:
    for x1,y1,x2,y2 in lines[0]:
      iterator += 1
      med_x1 += x1
      med_y1 += y1
      med_x2 += x2
      med_y2 += y2
    if iterator != 0:
      med_x1 /= iterator
      med_y1 /= iterator
      med_x2 /= iterator
      med_y2 /= iterator
  return(med_x1,med_y1,med_x2,med_y2)

class imageGrabber:

  ##Init function, create subscriber and required vars.
  def __init__(self):
    image_sub = rospy.Subscriber("/g500/camera1",Image,self.image_callback)
    self.bridge = CvBridge()
    self.lines = [[]]
    self.height=-1
    self.width=-1
    self.channels=-1

  ##Image received -> process the image
  def image_callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    self.height, self.width, self.channels = cv_image.shape
    
    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([50,100,0])
    upper_green = np.array([70,255,255])
    #binarize image
    bin_image = cv2.inRange(hsv, lower_green, upper_green) 

    edges_image = cv2.Canny(bin_image, 50, 150, apertureSize = 3)
   
    self.lines = cv2.HoughLinesP(edges_image, 1, np.pi/180,50,40,10)
    
    if self.lines != None:
      for x1,y1,x2,y2 in self.lines[0]:
        cv2.line(cv_image,(x1,y1),(x2,y2),(255,0,0),2)
    else:
      print "NONE!" 

    
    (med_x1,med_y1,med_x2,med_y2) = get_mediumLine( self.lines )
    cv2.line(cv_image,(med_x1,med_y1),(med_x2,med_y2),(0,0,255),2)

    cv2.imshow("Image window", cv_image)
    #cv2.imshow("Image Thresh", bin_image)
    #cv2.imshow("Image Edges", edges_image)

    cv2.waitKey(3)

  ##Return size of the image
  def getSize(self):
    return self.width,self.height

  def getLines( self ):
    return self.lines

def is_nonVerticalLine( line ):
  count = 0
  existNonVerticalLine = 0    
  if lines != None:
    for line in lines[0]:
      dx = line[0] - line[2]
      dy = line[1] - line[3]
      if dy != 0:
        theta = np.arctan(float(dx)/float(dy))
      else:
        theta = np.pi/2
      print "theta = ",theta,"line(",count,")"
      vline = 0
      if abs(theta) < 0.1:
        vline = 1
        print "Vertica: line(",count,")"
      count += 1
      if( vline == 0 ):
        existNonVerticalLine = 1
  return existNonVerticalLine

   

if __name__ == '__main__':
  #topic to command
  twist_topic="/g500/velocityCommand"
  #base velocity for the teleoperation (0.2 m/s) / (0.2rad/s)
  baseVelocity=0.5

  ##create the publisher
  rospy.init_node('pipeFollowing')
  pub = rospy.Publisher(twist_topic, TwistStamped,queue_size=1)
  
  ##wait for benchmark init service
  rospy.wait_for_service('/startBench')
  start=rospy.ServiceProxy('/startBench', Empty)
  
  ##wait for benchmark stop service
  rospy.wait_for_service('/stopBench')
  stop=rospy.ServiceProxy('/stopBench', Empty)

  #Create the imageGrabber
  IG=imageGrabber()
  
  start()
  while not rospy.is_shutdown():
    msg = TwistStamped()

    #get width x height of the last received image
    imwidth,imheight=IG.getSize()

    lines = IG.getLines( )

    if lines != None:
      existNonVerticalLine = is_nonVerticalLine(lines)
      #If every line is vertical, we move foward
      if (existNonVerticalLine == 0):
        msg.twist.linear.x = baseVelocity
        msg.twist.linear.y = 0
        msg.twist.linear.z = 0
        msg.twist.angular.z = 0.0

      #If no line is vertical, we move foward
      if (existNonVerticalLine == 1):
        msg.twist.linear.x = 0
        msg.twist.linear.y = 0
        msg.twist.linear.z = 0
        msg.twist.angular.z = 0.0
        print "Stop"

    pub.publish(msg)
    
    rospy.sleep(0.1)
  
  stop()

