
from app.repository import repository
from app.model.user import User

from flask import Blueprint, request

app_user = Blueprint('app_user', __name__)


@app_user.route('/user', methods=['POST'])
def insert():
    new_user = request.json

    user = User(new_user)
    user.validate()

    repository.insertOneUnique("users", user, ("email"))

    return {"message": "success"}


@app_user.route('/', methods=['GET'])
def getAll():
    return {"users": repository.getAllDocs("users")}
