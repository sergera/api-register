import json

from pymongo import MongoClient
import mongomock

from .exceptions import (CouldNotDeleteDocumentException,
                         CouldNotDeleteDocumentsException,
                         CouldNotGetDocumentException,
                         CouldNotGetDocumentsException,
                         CouldNotInsertDocumentException,
                         ExistingDocumentException,
                         CouldNotDropCollectionException,
                         CouldNotDropDatabaseException,)

class MongoRepository():
    """
    A class used to represent the MongoDB database
    It uses pymongo, and simplifies some of it's basic functionality

    Args:
        db_address (str):
            MongoDB's address
        db_name (str):
            the name of the database in this particular instance of MongoDB

    Attributes:
        db_address (str):
            MongoDB's address
        db_name (str):
            the name of the database in this particular instance of MongoDB
    """
    def __init__(self, db_address, db_name, test=None):
        self.db_address = db_address
        self.db_name = db_name
        self._db = None
        self._client = None
        if test:
            self.mock_connect()
        else:            
            self.connect()

    def mock_connect(self):
        self._client = mongomock.MongoClient()
        self._db = self._client.db

    def connect(self):
        self._client = MongoClient(self.db_address)
        self._db = self._client[self.db_name]

    def get_doc(self, collection_name, key):
        """Gets one document in a collection

        Args:
            collection_name (str):
                The name of the collection
            key (dict):
                one document with those keys assigned to those values will be fetched

        Returns:
            dict: Document   

        Raises:
            CouldNotGetDocumentException
                If it fails to retrieve the document
        """
        try:
            document = self._db[collection_name].find_one(key, {'_id': False})
            return document

        except:
            raise CouldNotGetDocumentException("Could not get document!")

    def get_docs(self, collection_name, key):
        """Gets documents in a collection with the specified key

        Args:
            collection_name (str):
                The name of the collection
            key (dict):
                Every document with those keys assigned to those values will be fetched

        Returns:
            list: Documents   

        Raises:
            CouldNotGetDocumentsException
                If it fails to retrieve documents
        """
        try:
            cursor = self._db[collection_name].find(key, {'_id': False})
            return list(cursor)

        except:
            raise CouldNotGetDocumentsException("Could not get documents!")

    def get_all_docs(self, collection_name):
        """Gets all documents in a collection

        Args:
            collection_name (str):
                The name of the collection

        Returns:
            list: All documents in collection   

        Raises:
            CouldNotGetDocumentsException
                If it fails to retrieve documents
        """
        try:
            cursor = self._db[collection_name].find({}, {'_id': False})
            return list(cursor)

        except:
            raise CouldNotGetDocumentsException("Could not get all documents!")

    def insert_one(self, collection_name, document):
        """Inserts one document in a collection

        Args:
            collection_name (str):
                Name of the collection
            document (dict):
                Document to be inserted

        Returns:
            dict: a status message

        Raises:
            CouldNotInsertDocumentException
                If it fails to insert the document
        """
        try:
            result = self._db[collection_name].insert_one(document.copy())
            return {"message": "Document Inserted!"}

        except:
            raise CouldNotInsertDocumentException("Could not insert document!")
        
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
                Name of the collection
            document (dict):
                Document to be inserted
            rules (dict, optional):
                Key rules
                
        Raises:
            ExistingDocumentException
                In case the defined keys are not unique in the collection
        """
        if rules:

            if "compound_key" in rules:
                #check if compound key is unique in the collection

                key_dict = { key: document[key] for key in rules["compound_key"] }
                found_document = self._db[collection_name].find_one(key_dict, {'_id': False})

                if found_document:
                    raise ExistingDocumentException("Compound key already exists in collection!")

            if "unique_keys" in rules:
                #check if all unique keys are individually unique in the collection

                key_list = [ { key: document[key] } for key in rules["unique_keys"] ]

                for key in key_list:
                    found_document = self._db[collection_name].find_one(key, {'_id': False})

                    if found_document:
                        raise ExistingDocumentException("Unique keys already exist in collection!")

            message = self.insert_one(collection_name, document)
            return message

        else:
            #insert document only if all fields are unique

            found_document = self._db[collection_name].find_one(document, {'_id': False})

            if found_document:
                raise ExistingDocumentException("Identical already document exists in collection!")

            else:
                message = self.insert_one(collection_name, document)
                return message

    def delete_one(self, collection_name, key):
        """Deletes one document

        Args:
            collection_name (str):
                Name of the collection
            key (dict):
                One document with those keys assigned to those values will be deleted
        """
        try:
            self._db[collection_name].delete_one(key)
            return {"message": "Document Deleted!"}

        except:
            raise CouldNotDeleteDocumentException('Could not delete document!')


    def delete_many(self, collection_name, key):
        """Deletes documents based on the specified key

        Args:
            collection_name (str):
                Name of the collection
            key (dict):
                Every document with those keys assigned to those values will be deleted
        """
        try:
            self._db[collection_name].delete_many(key)
            return {"message": "Documents Deleted!"}

        except:
            raise CouldNotDeleteDocumentsException('Could not delete documents!')

    def delete_all(self, collection_name):
        """Deletes all documents in a colletion

        Args:
            collection_name (str):
                Name of the collection
        """
        try:
            self._db[collection_name].delete_many({})
            return {"message": "All Documents Deleted!"}

        except:
            raise CouldNotDeleteDocumentsException('Could not delete all documents!')

    def drop_collection(self, collection_name):
        """
        Args:
            collection_name (str):
                The name of the collection
        """
        try:
            self._db.drop_collection(collection_name)
            return {"message": "Collection Droped!"}

        except:
            raise CouldNotDropCollectionException('Could not drop collection!')

    def drop_database(self, db_name):
        """
        Args:
            db_name (str):
                The name of the database
        """
        try:
            self._client.drop_database(db_name)
            return {"message": "Database Droped!"}

        except:
            raise CouldNotDropDatabaseException('Could not drop database!')