import rospy
from geometry_msgs.msg import Twist
import settings

pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)

def talker():

	# print("I am talking")
	# print(settings.Kp)
	global pub
	
	#rospy.init_node('talker', anonymous=True)
	#rate = rospy.Rate(10) # 10hz
	if (settings.err_x>0):
		if (settings.err_x<settings.x_thresh):
			settings.err_x=0.0
		elif (settings.err_x>settings.x_thresh):
			settings.err_x=settings.Kp*settings.err_x
	else:
		if (abs(settings.err_x)<settings.x_thresh):
			settings.err_x=0.0
		elif (abs(settings.err_x)>settings.x_thresh):
			settings.err_x=settings.Kp*settings.err_x
	# print("I am talking2 ")	
	# print(settings.err_x)	

	if (settings.err_y>0):
		if (settings.err_y<settings.x_thresh):
			settings.err_y=0.0
		elif (settings.err_y>settings.x_thresh):
			settings.err_y=settings.Kp*settings.err_y
	else:
			if (abs(settings.err_y)<settings.y_thresh):
				settings.err_y=0.0
			elif (abs(settings.err_y)>settings.y_thresh):
				 settings.err_y=settings.Kp*settings.err_y

	# print(settings.err_x)
	
	pub.publish(twist_obj(settings.err_y, settings.err_x, 0.0, 0.0, 0.0, 0.0))
        
def twist_obj(x,y,z,a,b,c):
	move_cmd=Twist()
	move_cmd.linear.x=x
	move_cmd.linear.y=y
	move_cmd.linear.z=z
	move_cmd.angular.x=a
	move_cmd.angular.y=b
	move_cmd.angular.z=c
	return move_cmd

def hover():
	global pub
	pub.publish(twist_obj(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))

def move_up():
	global pub
	pub.publish(twist_obj(0.0, 0.0, 0.1, 0.0, 0.0, 0.0))