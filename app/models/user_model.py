import re

from .exceptions import ValidationException

EMAIL_REGEX = re.compile("^(([a-zA-Z]|[0-9])+(-|_|\\.)?)+@[a-zA-Z]+(\\.[a-zA-Z]+)+$")

NAME_REGEX = re.compile("^[a-zA-Z]+(\\ ?[a-zA-Z]+)+$")

class UserModel():
    """
    A class used to represent a user model

    Args:
        user (dict):
            A dict containing the "email" and "name" keys

    Attributes:
        email (str):
            MongoDB's address
        name (str):
            Name of the database in this particular instance of MongoDB
    """
    def __init__(self, user):
        try:
            self.email = user["email"]
            self.name = user["name"]
        except:
            raise ValidationException("Missing Parameters!")

    def validate(self):
        """Validates user properties

        Returns:
            bool: True if it is valid

        Raises:
            ValidationException
                If any of the properties are not valid
        """
        if not EMAIL_REGEX.match(self.email):
            raise ValidationException("Email not valid!")

        if not NAME_REGEX.match(self.name):
            raise ValidationException("Name not valid!")

        return True

    def to_dict(self):
        """Makes a dict out of this object

        Returns:
            dict: with each key as a property from this object
        """
        return {"email": self.email, "name": self.name}