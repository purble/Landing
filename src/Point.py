class Point:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def display(self):
		return "("+str(self.x)+","+str(self.y)+")"

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def distTo(self, other):
		z = pow(self.x-other.x,2) + pow(self.x-other.x,2)
		return pow(z,.5)

	def connected(self, other, thresh):
		return self.distTo(other) <= thresh