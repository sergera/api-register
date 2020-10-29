from pymongo import MongoClient
import json

from .exceptions import ExistingDocumentException
from .exceptions import CouldNotInsertDocumentException
from .exceptions import CouldNotGetDocumentsException

class Mongo():
    """
    A class used to represent the MongoDB database.
    It uses pymongo, and simplifies some of it's basic functionality.

    Args:
        db_address (str):
            MongoDB's address.
        db_name (str):
            the name of the database in this particular instance of MongoDB.        

    Attributes:
        db_address (str):
            MongoDB's address.
        db_name (str):
            the name of the database in this particular instance of MongoDB.
    """
    def __init__(self, db_address, db_name):
        self.db_address = db_address
        self.db_name = db_name
        self.db = None
        self.connect()

    def connect(self):
        client = MongoClient(self.db_address)
        self.db = client[self.db_name]

    def get_all_docs(self, collection_name):
        """Gets all documents in a collection

        Args:
            collection_name (str):
                The name of the collection

        Returns:
            list: documents in collection   

        Raises:
            CouldNotGetDocumentsException
                If it fails to retrieve documents
        """
        try:
            cursor = self.db[collection_name].find({}, {'_id': False})
            return list(cursor)
        except:
            raise CouldNotGetDocumentsException("Could not get all documents!")

    def insert_one(self, collection_name, document):
        """Inserts one document in a collection

        Args:
            collection_name (str):
                The name of the collection
            document (dict):
                Document to be inserted

        Returns:
            dict: a status message

        Raises:
            CouldNotInsertDocumentException
                If it fails to insert the document
        """
        try:
            result = self.db[collection_name].insert_one(document)
            return {"message": "Document Inserted!"}
        except:
            raise CouldNotInsertDocumentException("Could not insert in database!")
        
    def insert_one_key(self, collection_name, document, rules=None):
        """Inserts one document in a collection, with rules for which fields are keys

        If no rules are passed, the whole document will be considered a key, and will 
        only be inserted if it's completely unique

        If the rules dict has a "compound_key" set, listed field names will be 
        considered a compound key
        
        If the rules dict has a "unique_keys" set, listed field names will each be 
        considered a key

        Args:
            collection_name (str):
                The name of the collection
            document (dict) :
                Document to be inserted
            rules (dict of sets, optional):
                Key rules
                
        Raises:
            ExistingDocumentException
                In case the defined keys are not unique in the collection
        """
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