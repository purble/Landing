def init():

	# ################# Settings for filtering noise via connected components ##################

	global size, thresh, cutoff, list_p # inc thresh at higher speeds but will include outliers

	# Good for slow speed to remove outliers

	size = 15   # size of queue of points
	thresh = 20  # distance between two points to be connected
	cutoff = 5 # size of connected component to look for atleast

	# Good for slow speed to remove outliers

	# size = 25   # size of queue of points
	# thresh = 5  # distance between two points to be connected
	# cutoff = 8 # size of connected component to look for atleast

	# good for high speeds but will include outliers

	# size = 25   # size of queue of points
	# thresh = 15  # distance between two points to be connected
	# cutoff = 12 # size of connected component to look for atleast

	# size = 30   # size of queue of points
	# thresh = 15  # distance between two points to be connected
	# cutoff = 12 # size of connected component to look for atleast

	# size = 20   # size of queue of points
	# thresh = 15  # distance between two points to be connected
	# cutoff = 8 # size of connected component to look for atleast

	list_p = []

	# improve code by instead of popping out last value pop a random value which is not in connected component if the new value is not in connected component
	# else pop value from connected component and insert a new one
	# and if found within connecting component stop processing whole 20 values again and again
	# and with some probability pop a value from connected component to keep refreshing it
	# in presence of noise it is not choosing pre exisiting connected so bias things towards by popping non-root connected value with more prob than connected comp
	# can include the the points from two concentric triangles off diff colors to get a more robust measure of center

	# ################################# Settings for PID Controller ####################################

	y_thresh = 5
	x_thresh = 5
	Kp = 0.01
	err_x = 0.0
	err_y = 0.0