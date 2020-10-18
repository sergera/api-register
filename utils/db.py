from pymongo import MongoClient

class Mongo():
	def __init__(self, dbAddress, dbName):
		self.dbAddress = dbAddress
		self.dbName = dbName
		self.db = None
		self.connect()

	def connect(self):
		try:
			client = MongoClient(self.dbAddress)
			self.db = client[self.dbName]
		except (pymongo.errors.ConnectionFailure):
			print("\nCould not connect to db")


	def insertOne(self, collectionName, document):
		try:
			result = self.db[collectionName].insert_one(document)
			print("\nUser Inserted! -> {0}".format(result.inserted_id))
			return result
		except:
			print("\nCould not insert in database")
		