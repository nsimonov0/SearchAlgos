from queue import PriorityQueue

class State(object):
	def __init__(self, value, parent, start = 0, goal = 0):
		self.children = []
		self.parent = parent
		self.value = value
		self.dist = 0
		if parent:
			self.start = parent.start
			self.goal = parent.goal
			self.path = parent.path[:] #Important to make copy of a list
			self.path.append(value)
		else:
			self.path = [value]
			self.start = start
			self.goal = goal

	def get_distance(self):
		pass

	def create_children(self):
		pass

class State_String(State):
	def __init__(self, value, parent, start = 0, goal = 0):
		super(State_String, self).__init__(value, parent, start, goal)
		self.dist = self.get_distance()

	def get_distance(self):
		if self.value == self.goal:
			return 0
		dist = 0
		for i in range(len(self.goal)):
			letter = self.goal[i]
			dist += abs(i - self.value.index(letter))
		return dist

	def create_children(self):
		if not self.children:
			for i in range(len(self.goal)-1):
				val = self.value 
				val = val[:i] + val[i+1] + val[i] + val[i+2:]
				child = State_String(val, self)
				self.children.append(child)

class AStar:
	def __init__(self, start, goal):
		self.path = []
		self.visitedq = []
		self.priorityq = PriorityQueue()
		self.start = start
		self.goal = goal

	def solve(self):
		start_state = State_String(self.start,0,self.start,self.goal)
		count = 0
		self.priorityq.put((0, count, start_state))
		while(not self.path and self.priorityq.qsize()):
			closest_child = self.priorityq.get()[2]
			closest_child.create_children()
			self.visitedq.append(closest_child.value)
			for child in closest_child.children:
				if child.value not in self.visitedq:
					count += 1
					if not child.dist:
						self.path = child.path
						break
					self.priorityq.put((child.dist, count, child))
		if not self.path:
			print("The goal is not possible to reach.")
		return self.path


if __name__ == "__main__":
	start = "olaikoinmnsi"
	goal = "nikolaisimon"
	a = AStar(start,goal)
	a.solve()
	for i in range(len(a.path)):
		print ("%d) " %i + a.path[i])


				