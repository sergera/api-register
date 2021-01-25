import json

from pymongo import MongoClient

from .exceptions import (CouldNotGetDocumentsException,
                         CouldNotInsertDocumentException,
                         ExistingDocumentException,)

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
    def __init__(self, db_address, db_name):
        self.db_address = db_address
        self.db_name = db_name
        self._db = None
        self._client = None
        self.connect()

    def connect(self):
        self._client = MongoClient(self.db_address)
        self._db = self._client[self.db_name]

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

    def insert_one_unique_fields(self, collection_name, document, field_sets):
        """Inserts a document with unique fields in a collection

        Args:
            collection_name (str):
                Name of the collection
            document (dict):
                Document to be inserted
            field_sets (list[set]):
                If there are no documents in the collection with any of the field_sets,
                the document will be inserted

        Raises:
            ExistingDocumentException
                In case the defined keys are not unique in the collection
        """
        for field_set in field_sets:
            unique_fields = { field: document[field] for field in field_set }
            found_document = self._db[collection_name].find_one(unique_fields, {"_id": False})
            if found_document:
                raise ExistingDocumentException("Unique fields already exist in collection!")

        message = self.insert_one(collection_name, document)
        return message