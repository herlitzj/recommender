class Calculator(object):

	def add(self, x, y):
		number_types = (int, long, float, complex)

		if isinstance(x, number_types) and isinstance(y, number_types):
			return x+y
		else:
			raise ValueError


	def sub(self, x, y):
		return x-y

	def mult(self, x, y):
		return x*y

	def div(self, x, y):
		return x/y

	def fact(self, x):
		if x == 1: return x
		else: return x * self.fact(x-1)
