class Command:
	"""
	TODO:
	The Command class represents a custom command that can be used by the bot. It includes essential information about the command, such as its name, description, function (the code to be executed when the command is invoked), and any options the command may have.
	"""
	def __init__(self, name, description, func, options=None):
		"""
		TODO:
		The __init__ method initializes the Command instance with the provided name, description, function, and options. If no options are provided, it initializes the options as an empty list.
		"""
		self.name = name
		self.description = description
		self.func = func
		self.options = options if options is not None else []

	def to_dict(self):
		"""
		TODO:
		The to_dict method converts the Command object into a dictionary format, which can be used for interacting with the Discord API. This method creates a dictionary with the command's name, description, and options. If there are any options available, it converts each option into a dictionary using the to_dict method of the Option class (not shown in the provided code). If there are no options, it sets the "options" key to None.
		"""
		return {
			"name": self.name,
			"description": self.description,
			"options": [option.to_dict() for option in self.options] if self.options else None,
		}