import rospy
from geometry_msgs.msg import Twist
import settings

def talker():

	global settings.y_thrsettings.err_xh, settings.x_thrsettings.err_xh, settings.Kp



	pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10) # 10hz
	if (settings.err_xs):
		if (settings.err_x<settings.x_thrsettings.err_xh):
			Self.settings.err_x=0.0
		else if (settings.err_x>settings.x_thrsettings.err_xh):
			Self.settings.err_x=settings.Kp*Self.settings.err_x
	else:
		if (Self.settings.err_x<settings.x_thrsettings.err_xh):
			Self.settings.err_x=0.0
		else if (Self.settings.err_x>settings.x_thrsettings.err_xh):
			Self.settings.err_x=-settings.Kp*Self.settings.err_x


	if (efs):
		if (Self.ef<settings.x_thrsettings.err_xh):
			Self.ef=0.0
		else if (Self.ef>settings.x_thrsettings.err_xh):
			Self.ef=settings.Kp*Self.ef
		else:
			if (Self.ef<settings.y_thrsettings.err_xh):
				Self.ef=0.0
			else if (Self.ef>settings.y_thrsettings.err_xh):
				Self.ef=-settings.Kp*Self.ef

	while not rospy.is_shutdown():
		hello_str = "hello world %s" % rospy.get_time()
		rospy.loginfo(hello_str)
		pub.publish(hello_str)
		rate.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
