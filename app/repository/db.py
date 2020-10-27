from pymongo import MongoClient
import json

from .exceptions import ExistingDocumentException
from .exceptions import CouldNotInsertDocumentException
from .exceptions import CouldNotGetDocumentsException

"""

Mongo Class

Receives an adress to the database and a database name on instantiation.

get_all_docs() - receives collection name as string.
             - returns a list of documents, with the internal MongoDB _id absent.

insert_one() - receives a collection name as string, and a document as dict.
            - returns a status string.

insert_one_key() 
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
        client = MongoClient(self.db_address)
        self.db = client[self.db_name]

    def get_all_docs(self, collection_name):
        try:
            cursor = self.db[collection_name].find({}, {'_id': False})
            return list(cursor)
        except:
            raise CouldNotGetDocumentsException("Could not get all documents!")

    def insert_one(self, collection_name, document):
        try:
            result = self.db[collection_name].insert_one(document)
            return {"message": "Document Inserted!"}
        except:
            raise CouldNotGetDocumentsException("Could not insert in database!")
        
    def insert_one_key(self, collection_name, document, rules):
        if rules:
            if "compound_key" in rules:
                #check if compound key is unique in the collection
                key_dict = { key: document[key] for key in rules["compound_key"] }
                found_document = self.db[collection_name].find_one(key_dict, {'_id': False})
                if found_document:
                    raise ExistingDocumentException("Compound key exists in collection!")

            if "unique_keys" in rules:
                #check if all unique keys are individually unique in the collection
                key_list = [ { key: document[key] } for key in rules["unique_keys"] ]
                for key in key_list:
                    found_document = self.db[collection_name].find_one(key, {'_id': False})
                    if found_document:
                        raise ExistingDocumentException("Unique keys exist in collection!")
            result = self.insert_one(collection_name, document)
            return result
        else:
            #insert document only if all fields are unique
            found_document = self.db[collection_name].find_one(document, {'_id': False})
            if found_document:
                raise ExistingDocumentException("Identical document exists in collection!")
            else:
                result = self.insert_one(collection_name, document)
                return result