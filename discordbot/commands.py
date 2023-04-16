class Command:
	def __init__(self, name, description, func, options=None):
		self.name = name
		self.description = description
		self.func = func
		self.options = options if options is not None else []
