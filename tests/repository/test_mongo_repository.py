import unittest

import pymongo

import sys
sys.path.append('/tools')
from tools.test_tools import mock_sub_object_public_methods as mock_public_methods
from app.repository.mongo_repository import MongoRepository
from app.repository.exceptions import (CouldNotGetDocumentException,
                                       CouldNotGetDocumentsException,
                                       CouldNotInsertDocumentException,
                                       ExistingDocumentException,
                                       CouldNotDeleteDocumentException,
                                       CouldNotDeleteDocumentsException,
                                       CouldNotDropDatabaseException,
                                       CouldNotDropCollectionException)

TEST_DATABASE_NAME = "test"
TEST_COLLECTION_NAME = "test"

class RepositoryTestCase(unittest.TestCase):
    
    def setUp(self):
        self.mongo = MongoRepository("mongodb://127.0.0.1:27017", TEST_DATABASE_NAME, test=True)
        self.dead_mongo = MongoRepository("mongodb://127.0.0.1:27017", TEST_DATABASE_NAME, test=True)
        """make dead_mongo use mutant libs whose public methods only raise exceptions"""
        mock_public_methods(self.dead_mongo, {"_client", "_db"}, failure=True)
            
    def tearDown(self):
        self.mongo.delete_all(TEST_COLLECTION_NAME)
        self.mongo.drop_database(TEST_DATABASE_NAME)

    def test_get_doc_success(self):
        user = {"email": "get@doc.com", "name": "get doc"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        gotten_user = self.mongo.get_doc(TEST_COLLECTION_NAME, user)
        self.assertEqual(gotten_user, user)

    def test_get_doc_failure(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        with self.assertRaises(CouldNotGetDocumentException): 
            self.dead_mongo.get_doc(TEST_COLLECTION_NAME, user)

    def test_get_docs_success(self):
        user = {"email": "get@docs.com", "name": "get docs"}
        for i in range(3):
            self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        gotten_users = self.mongo.get_docs(TEST_COLLECTION_NAME, user)
        self.assertEqual(len(gotten_users),3)

    def test_get_docs_failure(self):
        user = {"email": "get@docs.com", "name": "get docs name"}
        with self.assertRaises(CouldNotGetDocumentsException): 
            self.dead_mongo.get_docs(TEST_COLLECTION_NAME, user)

    def test_get_all_success(self):
        user = {"email": "get@all.docs", "name": "get all docs"}
        for i in range(3):
            self.mongo.insert_one("get_all_docs_test_collection", user)
        gotten_users = self.mongo.get_all_docs("get_all_docs_test_collection")
        self.assertEqual(len(gotten_users),3)
        self.mongo.delete_all("get_all_docs_test_collection")
        self.mongo.drop_collection("get_all_docs_test_collection")

    def test_get_all_failure(self):
        user = {"email": "get@all.docs", "name": "get all docs"}
        with self.assertRaises(CouldNotGetDocumentsException): 
            self.dead_mongo.get_all_docs(TEST_COLLECTION_NAME)

    def test_insert_one_user_success(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        gotten_user = self.mongo.get_doc(TEST_COLLECTION_NAME, user)
        self.assertEqual(gotten_user, user)

    def test_insert_one_user_failure(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        with self.assertRaises(CouldNotInsertDocumentException): 
            self.dead_mongo.insert_one(TEST_COLLECTION_NAME, user)

    def test_insert_unique_user_success(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.delete_many(TEST_COLLECTION_NAME, user)
        result = self.mongo.insert_one_key(TEST_COLLECTION_NAME, user)
        self.assertTrue("message" in result)

    def test_insert_unique_user_failure(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        with self.assertRaises(ExistingDocumentException):
            self.mongo.insert_one_key(TEST_COLLECTION_NAME, user)

    def test_insert_user_compound_key_success(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.delete_many(TEST_COLLECTION_NAME, user)
        rules = {"compound_key": {"email", "name"} }
        result = self.mongo.insert_one_key(TEST_COLLECTION_NAME, user, rules)
        self.assertTrue("message" in result)

    def test_insert_user_compound_key_failure(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        rules = {"compound_key": {"email", "name"} }
        with self.assertRaises(ExistingDocumentException): 
            self.mongo.insert_one_key(TEST_COLLECTION_NAME, user, rules)

    def test_insert_user_unique_keys_success(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.delete_many(TEST_COLLECTION_NAME, user)
        rules = {"unique_keys": {"email"} }
        result = self.mongo.insert_one_key(TEST_COLLECTION_NAME, user, rules)
        self.assertTrue("message" in result)

    def test_insert_user_unique_keys_failure(self):
        user = {"email": "correct@email.com", "name": "correct name"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        rules = {"unique_keys": {"email"} }
        with self.assertRaises(ExistingDocumentException): 
            self.mongo.insert_one_key(TEST_COLLECTION_NAME, user, rules)

    def test_delete_one_success(self):
        user = {"email": "tobedeleted@email.com", "name": "to be deleted"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        result = self.mongo.delete_one(TEST_COLLECTION_NAME, user)
        self.assertTrue("message" in result)

    def test_delete_one_failure(self):
        user = {"email": "tobedeleted@email.com", "name": "to be deleted"}
        with self.assertRaises(CouldNotDeleteDocumentException): 
            self.dead_mongo.delete_one(TEST_COLLECTION_NAME, user)
            
    def test_delete_many_success(self):
        user = {"email": "tobedeletedmany@email.com", "name": "to be deleted many"}
        for i in range(3):
            self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        result = self.mongo.delete_many(TEST_COLLECTION_NAME, user)
        self.assertTrue("message" in result)

    def test_delete_many_failure(self):
        user = {"email": "tobedeletedmany@email.com", "name": "to be deleted many"}
        with self.assertRaises(CouldNotDeleteDocumentsException): 
            self.dead_mongo.delete_many(TEST_COLLECTION_NAME, user)

    def test_delete_all_success(self):
        user = {"email": "tobedeletedall@email.com", "name": "to be deleted all"}
        self.mongo.insert_one(TEST_COLLECTION_NAME, user)
        result = self.mongo.delete_all(TEST_COLLECTION_NAME)
        self.assertTrue("message" in result)

    def test_delete_all_failure(self):
        user = {"email": "tobedeletedall@email.com", "name": "to be deleted all"}
        with self.assertRaises(CouldNotDeleteDocumentsException): 
            self.dead_mongo.delete_all(TEST_COLLECTION_NAME)

    def test_drop_database_success(self):
        result = self.mongo.drop_database(TEST_DATABASE_NAME)
        self.assertTrue("message" in result)

    def test_drop_database_failure(self):
        with self.assertRaises(CouldNotDropDatabaseException): 
            self.dead_mongo.drop_database(TEST_DATABASE_NAME)

    def test_drop_collection_success(self):
        result = self.mongo.drop_collection(TEST_COLLECTION_NAME)
        self.assertTrue("message" in result)

    def test_drop_collection_failure(self):
        with self.assertRaises(CouldNotDropCollectionException): 
            self.dead_mongo.drop_collection(TEST_DATABASE_NAME)


