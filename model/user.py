import re

"""

User Class

Receives an email as string and a name as string on instantiation.

validateEmail() - returns a valid boolean.

validateName() - returns a valid boolean.


"""

class User():
	def __init__(self, user):
		self.email = user["email"]
		self.name = user["name"]

	def validateEmail(self):
		regex = re.compile("^(([a-zA-Z]|[0-9])+(-|_|\\.)?)+@[a-zA-Z]+(\\.[a-zA-Z]+)+$")
		valid = regex.match(self.email)
		return valid

	def validateName(self):
		regex = re.compile("^[a-zA-Z]+(\\ ?[a-zA-Z]+)+$")
		valid = regex.match(self.name)
		return valid