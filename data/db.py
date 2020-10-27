from pymongo import MongoClient
import json

"""

Mongo Class

Receives an adress to the database and a database name on instantiation.

getAllDocs() - receives collection name as string.
			 - returns a list of documents, with the internal MongoDB _id absent.

insertOne() - receives a collection name as string, and a document as dict.
			- returns a status string.

insertOneKey() 
- receives a collection name as string, a document as dict, and an optional "rules" dict as a 3rd argument.
- the "rules" dict can have a "unique_keys" property, and/or a "compound_key" property.
- both properties can only have their values as a set.
- the set must have keys from the document (to be inserted) as strings.
- if there is a "rules" dict (3rd argument):
	-> the function will consider all of the fields in the "compound_key" set as a compound key.
	-> it will only insert the document if there is no other document with an identical compound key.
	-> the function will consider all of the fields in the "unique_keys" set as unique keys.
	-> it will only insert the document if there is no other document with any of the fields listed with identical values.
- if there is no "rules" dict (3rd argument):
    -> the function will consider all of the fields of the document as a compound key
    -> it will insert the document in the collection if there are no other documents identical to it.

"""

class Mongo():
	def __init__(self, db_address, db_name):
		self.db_address = db_address
		self.db_name = db_name
		self.db = None
		self.connect()

	def connect(self):
		try:
			client = MongoClient(self.db_address)
			self.db = client[self.db_name]
			print("\nSuccessfully connected to MongoDB database.")
		except (pymongo.errors.ConnectionFailure) as e:
			print("\nCould not connect to db: ",e)

	def getAllDocs(self, collection_name):
		try:
			result = self.db[collection_name].find({}, {'_id': False})
			print("Successfully retrieved all documents.")
			return list(result)
		except Exception as e:
			print("\nCould not retrieve all documents: ",e)

	def insertOne(self, collection_name, document):
		try:
			result = self.db[collection_name].insert_one(document)
			print("\nDocument Inserted! " + str(result.inserted_id))
			return "Document Inserted!"
		except Exception as e:
			print("\nCould not insert in database: ",e)
		
	def insertOneKey(self, collection_name, document, rules):
		if rules:
			document_already_exists = None
			if "compound_key" in rules:
				key_dict = { key: document[key] for key in rules["compound_key"] }
				cursor = self.db[collection_name].find(key_dict, {'_id': False})
				document_list = list(cursor)
				if document_list:
					document_already_exists = True

			if "unique_keys" in rules:
				key_list = [ { key: document[key] } for key in rules["unique_keys"] ]
				for key in key_list:
					cursor = self.db[collection_name].find(key, {'_id': False})
					document_list = list(cursor)
					if document_list:
						document_already_exists = True
						
			if document_already_exists:
				return {"message": "there is already a document in the dataBase"}
			else:
				result = self.insertOne(collection_name, document)
				return result
		else:
			cursor = self.db[collection_name].find(document, {'_id': False})
			document_list = list(cursor)
			if document_list:
				return {"message": "there is already a document in the dataBase"}
			else:
				result = self.insertOne(collection_name, document)
				return result