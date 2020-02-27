class DEQUE():
	def __init__(self):
		self.list = []

	def clean(self):
		self.list = []

	def get(self):
		return [] + self.list

	def get_by_i(self, index):
		return self.list[index]

	def push_back(self, item):
		self.list.append(item)

	def size(self):
		return len(self.list)

	def push_front(self, item):
		self.list.insert(0, item)

	def pop_back(self):
		if self.size() > 0:
			self.list.pop(-1)

	def pop_front(self):
		if self.size() > 0:
			self.list.pop(0)


class SPRITE_DEQUE(DEQUE):
	def __init__(self):
		super(SPRITE_DEQUE, self).__init__()

	def resizeAll(self, size):
		for i in range(self.size()):
			for j in range(len(self.list[i])):
				self.list[i][j].resize(size)
				if self.list[i][j].foldername is not None:
					self.list[i][j].load()