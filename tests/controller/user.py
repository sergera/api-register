import tempfile
import unittest
import json

from app import app

from unittest.mock import patch
from unittest.mock import MagicMock

class UserTestCase(unittest.TestCase):

    # def setUp(self):
    #     self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    #     app.app.config['TESTING'] = True
    #     self.test_app = app.app.test_client()
    #     self.user_to_insert = {
    #         "name": "functional test post user success", 
    #         "email": "functional_test_post_user@success.com"
    #     }
    #     self.test_app.delete("/users", data=self.user_to_insert) 

    def setUp(self):
        self.mocked_insert = MagicMock()
        with patch("app.controller.user", self.mocked_insert):

        self.mocked_get_all = MagicMock()
        with patch("app.controller.user.get_all", self.mocked_get_all):
            self.get_all = get_all

        self.mocked_root = MagicMock()
        with patch("app.controller.user.root", self.mocked_root):
            self.root = root


    with patch("app.controller.user", self.mocked_insert):
    def test_insert(self, mocked_insert):
        
        request = "<Request 'http://127.0.0.1:5000/user' [POST]>"

        response = self.insert(request)

        self.assertTrue()
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b"users" in response.data)
        # translated_json = json.loads(response.data)
        # self.assertTrue(isinstance(translated_json, dict))
        

    # def tearDown(self):
    #     self.test_app.post(
    #         "/users/delete", 
    #         data=json.dumps(self.user_to_insert, indent=4),
    #         content_type="application/json"
    #     ) 


    # def test_get_users(self):
    #     response = self.test_app.get("/users")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 200)
    #     self.assertEqual(response.content_type, "application/json")
    #     self.assertTrue(b"users" in response.data)
    #     translated_json = json.loads(response.data)
    #     self.assertTrue(isinstance(translated_json, dict))
    #     self.assertTrue(isinstance(translated_json["users"], list))
    #     if(translated_json["users"]):
    #         self.assertTrue(isinstance(translated_json["users"][0], dict))
    #         self.assertTrue("name" in translated_json["users"][0])
    #         self.assertTrue("email" in translated_json["users"][0])

    # def test_post_user_failure(self):
    #     response = self.test_app.post("/user")
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 500)
    #     self.assertEqual(response.content_type, "application/json")
    #     self.assertTrue(b"message" in response.data)

    # def test_post_user_success(self):
    #     response = self.test_app.post(
    #         "/user",
    #         data=json.dumps(self.user_to_insert, indent=4),
    #         content_type="application/json"
    #     )
    #     statuscode = response.status_code
    #     self.assertEqual(statuscode, 200)
    #     self.assertEqual(response.content_type, "application/json")
    #     self.assertTrue(b"message" in response.data)