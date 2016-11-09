#!/usr/bin/env python
from __future__ import print_function
import roslib
#roslib.load_manifest('my_package') # no longer needed on catkin
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import matplotlib.pyplot as plt
import math
from random import randint

from Point import Point
from shape_detection import process
import settings
# from ORB_features import process

orb = cv2.ORB_create()
ref = cv2.imread('/root/images/H1.png')
kp2 = orb.detect(ref,None)
kp2, des2 = orb.compute(ref, kp2)

class image_converter:

	def __init__(self):
		#self.image_pub = rospy.Publisher("image_topic_2",Image)
		self.image_pub = rospy.Publisher("/image_converter/output_video",Image,queue_size=10)
		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber("/ardrone/bottom/image_raw",Image,self.callback)
		# self.image_sub = rospy.Subscriber("/ardrone/front/image_raw",Image,self.callback)

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		img_ = process(cv_image) # shape detection

		# global orb, des2
		# img_ = process(cv_image, orb, des2) # ORB feature matching with ref image
		
		try:
			#self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
			# self.image_pub.publish(self.bridge.cv2_to_imgmsg(img_, "8UC1"))
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(img_, "bgr8"))
		except CvBridgeError as e:
			print(e)

def main(args):
	ic = image_converter()
	rospy.init_node('image_converter', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
		cv2.destroyAllWindows()

if __name__ == '__main__':
	settings.init()
	for i in range(settings.size): settings.list_p = [Point(randint(0,1000), randint(0,1000))] + settings.list_p
	print("Hello")
	print(len(settings.list_p))
	main(sys.argv)