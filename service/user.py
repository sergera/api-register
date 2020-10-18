import sys
sys.path.insert(0, './utils/db.py')

from utils import db


def insert(user):
	database = db.Mongo("mongodb://127.0.0.1:27017","cadastro")
	result = database.insertOne('users',user)
	return "\nUser inserted! ".format(result.inserted_id) if result.inserted_id else "\nError: User Not Inserted!"
	
def getAll():
	pass