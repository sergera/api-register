from pymongo import MongoClient

def mongo():
	client = MongoClient('mongodb://127.0.0.1:27017')
	return client.cadastro