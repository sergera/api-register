import unittest

from app.model.exceptions import ValidationException
from app.model.user import User


class UserTestCase(unittest.TestCase):
    """A Test of the Validation Regex
    
    Testing if the email and name regex patterns are responding as intended
    """
    def test_correct(self):
        correct = {"email": "correct@email.com", "name": "correct name"}
        new_user = User(correct)
        self.assertTrue(new_user.validate())

    def test_to_dict(self):
        correct = {"email": "correct@email.com", "name": "correct name"}
        new_user = User(correct)
        user_dict = new_user.to_dict()
        self.assertTrue(user_dict["email"] == correct["email"] and user_dict["name"] == correct["name"])

    def test_name_space_before(self):
        space_before_name = {"email": "correct@email.com", "name": " incorrect name"}
        new_user = User(space_before_name)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_name_space_after(self):
        space_after_name = {"email": "correct@email.com", "name": "incorrect name "}
        new_user = User(space_after_name)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_name_double_space(self):
        double_space = {"email": "correct@email.com", "name": "incorrect  name"}
        new_user = User(double_space)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_name_dot(self):
        dot = {"email": "correct@email.com", "name": "incorrect.name"}
        new_user = User(dot)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_name_number(self):
        number = {"email": "correct@email.com", "name": "incorrect 234 name"}
        new_user = User(number)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_space_before(self):
        space_before_email = {"email": " incorrect@email.com", "name": "correct name"}
        new_user = User(space_before_email)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_space_after(self):
        space_after_email = {"email": "incorrect@email.com ", "name": "correct name"}
        new_user = User(space_after_email)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_space_before_at(self):
        space_before_at = {"email": "incorrect @email.com", "name": "correct name"}
        new_user = User(space_before_at)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_space_after_at(self):
        space_after_at = {"email": "incorrect@ email.com", "name": "correct name"}
        new_user = User(space_after_at)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_space_before_dot(self):
        space_before_dot = {"email": "incorrect@email .com", "name": "correct name"}
        new_user = User(space_before_dot)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_space_after_dot(self):
        space_after_dot = {"email": "incorrect@email. com", "name": "correct name"}
        new_user = User(space_after_dot)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_no_dot(self):
        no_dot = {"email": "incorrect@emailcom", "name": "correct name"}
        new_user = User(no_dot)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_no_at(self):
        no_at = {"email": "incorrectemail.com", "name": "correct name"}
        new_user = User(no_at)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_double_dot(self):
        double_dot = {"email": "incorrect@email..com", "name": "correct name"}
        new_user = User(double_dot)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_double_at(self):
        double_at = {"email": "incorrect@@email.com", "name": "correct name"}
        new_user = User(double_at)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_two_ats(self):
        two_ats = {"email": "incorrect@email@what.com", "name": "correct name"}
        new_user = User(two_ats)
        with self.assertRaises(ValidationException):
            new_user.validate()

    def test_email_at_dot(self):
        at_dot = {"email": "incorrect@.email.com", "name": "correct name"}
        new_user = User(at_dot)
        with self.assertRaises(ValidationException):
            new_user.validate()