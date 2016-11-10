import rospy
from geometry_msgs.msg import Twist
import settings

def talker():

	 # global settings.y_thresh, settings.x_thresh, settings.err_x, settings.Kp, settings.err_y
	

	print("I am talking")
	print(settings.Kp)

	pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
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
	print("I am talking2 ")	
	print(settings.err_x)	

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

	print(settings.err_x)	


	move_cmd=Twist()
	# move_cmd.linear.x=-1*settings.err_y
	# move_cmd.linear.y=settings.err_x
	move_cmd.linear.x=settings.err_y
	move_cmd.linear.y=settings.err_x
	move_cmd.linear.z=0.0
	move_cmd.angular.x=0.0
	move_cmd.angular.y=0.0
	move_cmd.angular.z=0.0


	
	pub.publish(move_cmd)
        



# if __name__ == '__main__':
# 	try:
# 		talker()
# 	except rospy.ROSInterruptException:
# 		pass
