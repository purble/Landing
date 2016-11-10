# http://www.pyimagesearch.com/2016/02/01/opencv-center-of-contour/
# http://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
# https://solarianprogrammer.com/2015/05/08/detect-red-circles-image-using-opencv/
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html
# http://docs.opencv.org/trunk/d7/d4d/tutorial_py_thresholding.html

import argparse
import imutils
import cv2
import numpy as np
from Point import Point
from random import randint
from WtUF import UF
import settings

import rospy
from geometry_msgs.msg import Twist

from codePID import talker

def process(image):

	pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)

	# image = cv2.imread('/root/images/shapes_and_colors.jpg')
	# image = cv2.imread('/root/images/circle.png')
	# image = cv2.imread('/root/images/conc1.jpg')
	# image = cv2.imread('/root/images/conc3.png')

	# image = cv2.imread(imaeg_)

	######## prepare mask for black colors in image #########
	
	# convert image from BGR to HSV
	image = cv2.GaussianBlur(image, (5,5), 0)
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	ht, wd, ch = image.shape
	# print(ht,wd,ch)

	# define range of black color in HSV
	# lower_black = np.array([0,0,0])
	# upper_black = np.array([180,255,30])

	# define range of yellow color in HSV
	# lower_yellow = np.array([20,80,80])
	# upper_yellow = np.array([35,255,255])

	# define range of blue color in HSV
	lower_blue = np.array([100,80,80])
	upper_blue = np.array([110,255,255])

	# define range of red color in HSV
	# lower_red = np.array([165,80,80])
	# upper_red = np.array([180,255,255])

	# Threshold the HSV image to get only black colors
	# mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	# mask = cv2.inRange(hsv, lower_red, upper_red)

	# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# blurred = cv2.GaussianBlur(gray, (5,5), 0)
	# thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)[1]

	# cv2.imshow("Image Window", image)
	# cv2.waitKey()

	# cv2.imshow("Image Window : gray", gray)
	# cv2.waitKey()

	# cv2.imshow("Image Window : blurred", blurred)
	# cv2.waitKey()

	# cv2.imshow("Image Window : thresh", thresh)
	# cv2.waitKey()

	# cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# added = False
	# loop over the contours
	detected = False

	for c in cnts:

		peri = cv2.arcLength(c, True)
		area = cv2.contourArea(c)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)

		# print("peri= ", peri, " area= ", area, " sides= ", len(approx))

		# print(len(approx))
		# if len(approx) <= 4 or len(approx) > 10: continue
		if (len(approx) == 3 or len(approx) == 4 or len(approx) == 5) and area > 1000.0 and peri > 50.0 and peri < 1500.0:
		# if (len(approx) == 3 or len(approx) == 4):
		# if (len(approx) == 3):

			print(cv2.isContourConvex(c))

			print("peri= ", peri, " area= ", area, " sides= ", len(approx))

			# compute the center of contour
			M = cv2.moments(c)
			
			# draw the contour and center of the shape on the image
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])

			c = c.astype("int")
			cv2.drawContours(image, [c], -1, (0,255,0), 2)

			# added = True
			# settings.list_p = [Point(cX, cY)] + settings.list_p
			# settings.list_p.pop()
			
			cv2.circle(image, (cX, cY), 3, (0,255,0), -1)
			cv2.line(image, (wd/2, ht/2), (cX, cY), (136,0,108), 2)

			detected = True

			settings.err_x = cX-(wd/2)
			settings.err_y = cY-(ht/2)
			print(wd/2, ht/2, cX, cY, (cX-(wd/2)), (cY-(ht/2)))
			talker()

	if (not detected):
		move_cmd=Twist()
		move_cmd.linear.x=0.0
		move_cmd.linear.y=0.0
		move_cmd.linear.z=0.0
		move_cmd.angular.x=0.0
		move_cmd.angular.y=0.0
		move_cmd.angular.z=0.0
		print("Hover")
		pub.publish(move_cmd)		

	# res = CC_mean()
	# if res.x != -1 and res.y!=-1:
	# 	cv2.circle(image, (res.x, res.y), 3, (0,255,0), -1)
	# 	cv2.line(image, (wd/2, ht/2), (res.x, res.y), (136,0,108), 2)
	# 	settings.err_wd = res.x-(wd/2)
	# 	settings.err_ht = res.y-(ht/2)
	# 	print(wd/2, ht/2, res.x, res.y, (res.x-(wd/2)), (res.y-(ht/2)))
	# else:
	# 	cv2.circle(image, (wd/2, ht/2), 3, (0,0,255), -1)

 # 	if not added: 
 # 		settings.list_p.pop()
 # 		settings.list_p = [Point(randint(0,wd), randint(0,ht))] + settings.list_p

	return image
	# return mask

def CC_mean():
	uf = UF(settings.list_p)
	for i in range(len(settings.list_p)):
		for j in range(i):
			if settings.list_p[i].connected(settings.list_p[j], settings.thresh):
				uf.union(i, j)
				break

	if uf.maxSize() < settings.cutoff: return Point(-1,-1)
	else:
		connP = uf.getConnP()
		
		# #### Take avg of all points in biggest connected components #######

		# X = []
		# Y = []
		# print("=>", connP)
		# for i in connP:
		# 	X = X + [settings.list_p[i].getX()]
		# 	Y = Y + [settings.list_p[i].getY()]
		# X_ = sum(X)/len(X)
		# Y_ = sum(Y)/len(Y)

		# #### Return the coordinates of last added point ######

		X_ = settings.list_p[connP[0]].getX()
		Y_ = settings.list_p[connP[0]].getY()

		return Point(X_,Y_)