import sys
sys.path.insert(0, './utils/db.py')

from utils import db


def getUsers():
	pass

def insertUser(user):
	database = db.mongo()
	result = database.users.insert_one(user)
	print('Created {0}'.format(result.inserted_id))



	return 'user inserted!'