import sys
sys.path.insert(0, "./../utils/valid.py")
sys.path.insert(0, "./../utils/format.py")

from utils import valid
from utils import formatString
from service import user as userService


def insert(user):
	validEmail = valid.email(user['email'])
	#sometimes useful because of the request rate limit at the external email validation api
	#validEmail = True
	validName = valid.alphabeticSpaced(user["name"])
	user["name"] = formatString.name(user["name"])
	if(validEmail and validName):
		return userService.insert(user)
	else:
		inputStatus = []
		if(not validEmail):
			inputStatus.append("Invalid Email")
		if(not validName):
			inputStatus.append("Invalid Name")
		status = formatString.error(inputStatus)
		return status

def getAll():
	return "users!"