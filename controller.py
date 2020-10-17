

import sys
sys.path.insert(0, './utils/valid.py')

from utils import valid
from service import insertUser as insertUserService

def getUsers():
	return 'Hello, World!'

def insertUser(user):
	#check email
	email = user['email']
	validEmail = valid.email(email)
	#insert user
	return insertUserService(user) if validEmail else 'Invalid Email'