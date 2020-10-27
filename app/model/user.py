import re

from .exceptions import ValidationException

EMAIL_REGEX = re.compile("^(([a-zA-Z]|[0-9])+(-|_|\\.)?)+@[a-zA-Z]+(\\.[a-zA-Z]+)+$")

NAME_REGEX = re.compile("^[a-zA-Z]+(\\ ?[a-zA-Z]+)+$")

class User():
    """

    User Class

    Receives an email as string and a name as string on instantiation.

    validate() - returns True if the fields are validated, raises an Exception otherwise.

    to_json() - returns a dict with the object properties as attributes.

    """
    def __init__(self, user):
        self.email = user["email"]
        self.name = user["name"]

    def validate(self):
        if not self.email or not EMAIL_REGEX.match(self.email):
            raise ValidationException("Email not valid!")

        if not self.name or not NAME_REGEX.match(self.name):
            raise ValidationException("Name not valid!")

        return True

    def to_dict(self):
        return {"email": self.email, "name": self.name}