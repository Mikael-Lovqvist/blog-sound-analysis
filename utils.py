
class counting_iterator:
	def __init__(self):
		self.value = 0
		self.source = None

	def __call__(self, source):
		self.source = source
		return self

	def __iter__(self):
		return self

	def __next__(self):
		value = next(self.source)
		self.value += 1
		return value
