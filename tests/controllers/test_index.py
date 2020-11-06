import tempfile
import unittest

from app import app

class IndexTestCase(unittest.TestCase):
    """A test of the basic index route response

    Tests if the welcome route is responding 200, application/json, 
    and has data in response
    """
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.test_app = app.app.test_client()

    def test_index(self):
        response = self.test_app.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_index_content_type(self):
        response = self.test_app.get("/")
        self.assertEqual(response.content_type, "application/json")

    def test_index_data(self):
        response = self.test_app.get("/")
        self.assertTrue(b"message" in response.data)