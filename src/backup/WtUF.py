from Point import Point

class UF:
	
	def __init__(self, list_p):
		self.id = [i for i in range(len(list_p))]
		self.wt = [1] * len(list_p)
		self.maxSz = 1
		self.root = -1

	def union(self, a, b):
		p = self.find(a)
		q = self.find(b)
		if (self.wt[p] >= self.wt[q]): 
			self.id[q] = p
			self.wt[p] = self.wt[p] + self.wt[q]
			if self.maxSz < self.wt[p]:
				self.maxSz = self.wt[p]
				self.root = p
		else:
			self.id[p] = q
			self.wt[q] = self.wt[q] + self.wt[p]
			if self.maxSz < self.wt[q]:
				self.maxSz = self.wt[q]
				self.root = q

	def find(self, n):
		while (n != self.id[n]): n = self.id[n]
		return n

	def maxSize(self):
		return self.maxSz

	def connected(self, p, q):
		return self.find(p)==self.find(q)

	def getConnP(self):
		res = []
		for i in range(len(self.id)):
			if self.connected(i, self.root):
				res = res + [i]
		return res