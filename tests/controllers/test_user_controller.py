import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import json

import os
DB_NAME = os.environ.get("DB_NAME")

from app.repository import repository
from app.repository.mongo_repository import MongoRepository
from app import app

class UserControllerTestCase(unittest.TestCase):
    """

    """
    def setUp(self):
        #create test client
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.test_app = app.app.test_client()
        #mock repository
        self.mocked_repository = MagicMock()

    def test_get_users(self):
        mocked_response = [
                {"name": "nathaniel", "email": "nathaniel@email.com"},
                {"name": "jober", "email": "jober@email.com"}
            ]
        with patch("app.controllers.user_controller.repository", self.mocked_repository):
            self.mocked_repository.get_all_docs.return_value = mocked_response
            response = self.test_app.get("/users")

            statuscode = response.status_code
            self.assertEqual(statuscode, 200)
            self.assertEqual(response.content_type, "application/json")
            self.assertTrue(b"users" in response.data)
            translated_json = json.loads(response.data)
            self.assertTrue(isinstance(translated_json, dict))
            self.assertTrue(isinstance(translated_json["users"], list))
            self.assertTrue(isinstance(translated_json["users"][0], dict))
            self.assertTrue("name" in translated_json["users"][0])
            self.assertTrue("email" in translated_json["users"][0])
            self.assertEqual(translated_json["users"], mocked_response)

    def test_post_user(self):
        mocked_response = {"message": "success!"}
        user_to_insert = {
            "name": "functional test post user success", 
            "email": "functional_test_post_user@success.com"
        }
        with patch("app.controllers.user_controller.repository", self.mocked_repository):
            response = self.test_app.post(
                "/user",
                data=json.dumps(user_to_insert, indent=4),
                content_type="application/json"
            )

            statuscode = response.status_code
            self.assertEqual(response.content_type, "application/json")
            self.assertEqual(statuscode, 200)
            self.assertTrue(b"message" in response.data)
            translated_json = json.loads(response.data)
            self.assertEqual(translated_json, mocked_response)