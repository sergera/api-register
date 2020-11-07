import unittest

import pymongo

from unittest.mock import patch
from unittest.mock import MagicMock

from app.repository.mongo_repository import MongoRepository
from app.repository.exceptions import (CouldNotGetDocumentsException,
                                       CouldNotInsertDocumentException,
                                       ExistingDocumentException,)

import os
DB_NAME = os.environ.get("DB_NAME")
TEST_COLLECTION_NAME = "test"

class RepositoryTestCase(unittest.TestCase):
    """
    Tests repository interface with mocked pymongo
    """
    def setUp(self):
        #mock interface client
        self.mocked_mongo = MagicMock()
        with patch("app.repository.mongo_repository.MongoClient", self.mocked_mongo):
            self.mongo = MongoRepository("mongodb://127.0.0.1:27017", DB_NAME)
        #mock interface db
        self.mocked_db = self.mocked_mongo()[DB_NAME]
        #mock interface collection
        self.mocked_collection = MagicMock()
        self.mocked_db.__getitem__.return_value = self.mocked_collection

    def test_get_all_success(self):
        key = {"email": "get@all.docs", "name": "get all docs"}
        returned_users = ["we have returned"]

        self.mocked_collection.find.return_value = returned_users

        gotten_users = self.mongo.get_all_docs(TEST_COLLECTION_NAME)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find.assert_called_once_with({}, {"_id": False})
        self.assertEqual(gotten_users, returned_users)

    def test_get_all_failure(self):
        key = {"email": "get@all.docs", "name": "get all docs"}

        self.mocked_collection.find.side_effect = Exception("oops")

        with self.assertRaises(CouldNotGetDocumentsException):
            self.mongo.get_all_docs(TEST_COLLECTION_NAME)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find.assert_called_once_with({}, {"_id": False})

    def test_insert_one_user_success(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        returned_message = {"message": "Document Inserted!"}

        self.mocked_collection.insert_one.return_value = returned_message

        response = self.mongo.insert_one(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_one_user_failure(self):
        document = {"email": "correct@email.com", "name": "correct name"}

        self.mocked_collection.insert_one.side_effect = Exception("oops")

        with self.assertRaises(CouldNotInsertDocumentException):
            self.mongo.insert_one(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.insert_one.assert_called_once_with(document)


    def test_insert_one_unique_fields(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        unique_fields = [{"email", "name"}]
        returned_message = {"message": "Document Inserted!"}

        self.mocked_collection.find_one.return_value = None
        self.mocked_collection.insert_one.return_value = returned_message

        response = self.mongo.insert_one_unique_fields(TEST_COLLECTION_NAME, document, unique_fields)

        self.mocked_db.__getitem__.assert_called_with(TEST_COLLECTION_NAME)
        self.assertEqual(self.mocked_db.__getitem__.call_count, 2)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_one_unique_fields_failure(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        unique_fields = [{"email", "name"}]

        self.mocked_collection.find_one.return_value = document
        
        with self.assertRaises(ExistingDocumentException):
            self.mongo.insert_one_unique_fields(TEST_COLLECTION_NAME, document, unique_fields)