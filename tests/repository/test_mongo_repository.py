import unittest

import pymongo

from unittest.mock import patch
from unittest.mock import MagicMock

from app.repository.mongo_repository import MongoRepository
from app.repository.exceptions import (CouldNotGetDocumentException,
                                       CouldNotGetDocumentsException,
                                       CouldNotInsertDocumentException,
                                       ExistingDocumentException,
                                       CouldNotDeleteDocumentException,
                                       CouldNotDeleteDocumentsException,
                                       CouldNotDropDatabaseException,
                                       CouldNotDropCollectionException)

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

    def test_get_doc_success(self):
        key = {"email": "get@doc.com", "name": "get doc"}
        returned_user = "i have returned"

        self.mocked_collection.find_one.return_value = returned_user

        gotten_user = self.mongo.get_doc(TEST_COLLECTION_NAME, key)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find_one.assert_called_once_with(key, {"_id": False})
        self.assertEqual(gotten_user, returned_user)

    def test_get_doc_failure(self):
        key = {"email": "correct@email.com", "name": "correct name"}

        self.mocked_collection.find_one.side_effect = Exception("oops")

        with self.assertRaises(CouldNotGetDocumentException): 
            self.mongo.get_doc(TEST_COLLECTION_NAME, key)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find_one.assert_called_once_with(key, {"_id": False})

    def test_get_docs_success(self):
        key = {"email": "get@docs.com", "name": "get docs"}
        returned_users = ["we have returned"]

        self.mocked_collection.find.return_value = returned_users

        gotten_users = self.mongo.get_docs(TEST_COLLECTION_NAME, key)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find.assert_called_once_with(key, {"_id": False})
        self.assertEqual(gotten_users, returned_users)

    def test_get_docs_failure(self):
        key = {"email": "get@docs.com", "name": "get docs name"}

        self.mocked_collection.find.side_effect = Exception("oops")

        with self.assertRaises(CouldNotGetDocumentsException): 
            self.mongo.get_docs(TEST_COLLECTION_NAME, key)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.find.assert_called_once_with(key, {"_id": False})

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


    def test_insert_unique_user_success(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        returned_message = {"message": "Document Inserted!"}

        self.mocked_collection.find_one.return_value = None
        self.mocked_collection.insert_one.return_value = returned_message

        response = self.mongo.insert_one_key(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_with(TEST_COLLECTION_NAME)
        self.assertEqual(self.mocked_db.__getitem__.call_count, 2)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_unique_user_failure(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        
        self.mocked_collection.find_one.return_value = document
        
        with self.assertRaises(ExistingDocumentException):
            self.mongo.insert_one_key(TEST_COLLECTION_NAME, document)

    def test_insert_user_compound_key_success(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        rules = { "compound_key": {"email", "name"} }
        returned_message = {"message": "Document Inserted!"}

        self.mocked_collection.find_one.return_value = None
        self.mocked_collection.insert_one.return_value = returned_message

        response = self.mongo.insert_one_key(TEST_COLLECTION_NAME, document, rules)

        self.mocked_db.__getitem__.assert_called_with(TEST_COLLECTION_NAME)
        self.assertEqual(self.mocked_db.__getitem__.call_count, 2)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_user_compound_key_failure(self):
        document = {"email": "correct@email.com", "name": "correct name"}

        self.mocked_collection.find_one.return_value = document

        with self.assertRaises(ExistingDocumentException):
            self.mongo.insert_one_key(TEST_COLLECTION_NAME, document)

    def test_insert_user_unique_keys_success(self):
        document = {"email": "correct@email.com", "name": "correct name"}
        rules = { "compound_key": {"email", "name"} }
        returned_message = {"message": "Document Inserted!"}

        self.mocked_collection.find_one.return_value = None
        self.mocked_collection.insert_one.return_value = returned_message

        response = self.mongo.insert_one_key(TEST_COLLECTION_NAME, document, rules)

        self.mocked_db.__getitem__.assert_called_with(TEST_COLLECTION_NAME)
        self.assertEqual(self.mocked_db.__getitem__.call_count, 2)
        self.mocked_collection.insert_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_insert_user_unique_keys_failure(self):
        document = {"email": "correct@email.com", "name": "correct name"}

        self.mocked_collection.find_one.return_value = document

        with self.assertRaises(ExistingDocumentException):
            self.mongo.insert_one_key(TEST_COLLECTION_NAME, document)

    def test_delete_one_success(self):
        document = {"email": "tobedeleted@email.com", "name": "to be deleted"}
        returned_message = {"message": "Document Deleted!"}

        self.mocked_collection.delete_one.return_value = {"message": "success"}

        response = self.mongo.delete_one(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_with(TEST_COLLECTION_NAME)
        self.mocked_collection.delete_one.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_delete_one_failure(self):
        document = {"email": "tobedeleted@email.com", "name": "to be deleted"}

        self.mocked_collection.delete_one.side_effect = Exception("oops")

        with self.assertRaises(CouldNotDeleteDocumentException):
            self.mongo.delete_one(TEST_COLLECTION_NAME, document)
            
    def test_delete_many_success(self):
        document = {"email": "tobedeletedmany@email.com", "name": "to be deleted many"}
        returned_message = {"message": "Documents Deleted!"}

        self.mocked_collection.delete_many.return_value = {"message": "success"}

        response = self.mongo.delete_many(TEST_COLLECTION_NAME, document)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.delete_many.assert_called_once_with(document)
        self.assertEqual(returned_message, response)

    def test_delete_many_failure(self):
        document = {"email": "tobedeletedmany@email.com", "name": "to be deleted many"}

        self.mocked_collection.delete_many.side_effect = Exception("oops")

        with self.assertRaises(CouldNotDeleteDocumentsException): 
            self.mongo.delete_many(TEST_COLLECTION_NAME, document)

    def test_delete_all_success(self):
        document = {"email": "tobedeletedall@email.com", "name": "to be deleted all"}
        returned_message = {"message": "All Documents Deleted!"}

        self.mocked_collection.delete_many.return_value = {"message": "success"}

        response = self.mongo.delete_all(TEST_COLLECTION_NAME)

        self.mocked_db.__getitem__.assert_called_once_with(TEST_COLLECTION_NAME)
        self.mocked_collection.delete_many.assert_called_once_with({})
        self.assertEqual(returned_message, response)
        

    def test_delete_all_failure(self):
        document = {"email": "tobedeletedall@email.com", "name": "to be deleted all"}

        self.mocked_collection.delete_many.side_effect = Exception("oops")

        with self.assertRaises(CouldNotDeleteDocumentsException): 
            self.mongo.delete_all(TEST_COLLECTION_NAME)

    def test_drop_database_success(self):
        returned_message = {"message": "Database Droped!"}

        self.mocked_mongo().drop_database.return_value = {"message": "success"}

        result = self.mongo.drop_database(DB_NAME)

        self.assertEqual(returned_message, result)

    def test_drop_database_failure(self):
        self.mocked_mongo().drop_database.side_effect = Exception("oops")

        with self.assertRaises(CouldNotDropDatabaseException): 
            result = self.mongo.drop_database(DB_NAME)

    def test_drop_collection_success(self):
        returned_message = {"message": "Collection Droped!"}

        self.mocked_db.drop_collection.return_value = {"message": "success"}

        result = self.mongo.drop_collection(DB_NAME)

        self.assertEqual(returned_message, result)

    def test_drop_collection_failure(self):
        self.mocked_db.drop_collection.side_effect = Exception("oops")

        with self.assertRaises(CouldNotDropCollectionException): 
            self.mongo.drop_collection(DB_NAME)