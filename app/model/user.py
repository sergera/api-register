import re

from .exceptions import ValidationException

EMAIL_REGEX = re.compile("^(([a-zA-Z]|[0-9])+(-|_|\\.)?)+@[a-zA-Z]+(\\.[a-zA-Z]+)+$")

NAME_REGEX = re.compile("^[a-zA-Z]+(\\ ?[a-zA-Z]+)+$")


class User:
    """
    Class that ...

    Attributes:
            email (str): Email do usário
            name (str): Nome do usário
    """

    def __init__(self, data):
        self.email = data.get("email")
        self.name = data.get("name")

    def validate(self):
        """Validate all the fields of the model. Raises a Exception if any inconsistence is found."""

        if not self.email or not EMAIL_REGEX.match(self.email):
            raise ValidationException("Email not valid!")

        if not self.name or not NAME_REGEX.match(self.name):
            raise ValidationException("Name not valid!")

        return True

    def to_json(self):
        return {"email": email, "name": name}
