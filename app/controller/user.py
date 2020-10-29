from flask import Blueprint, request

from app.model.user import User
from app.repository import repository

app_user = Blueprint('app_user', __name__)

@app_user.route('/user', methods=['POST'])
def insert():
	"""
	Validates and inserts user
	"""
    new_user = request.json
    user = User(new_user)
    user.validate()
    repository.insert_one_key("users", user.to_dict(), {"unique_keys": {"email"}})
    return {"message": "success"}

@app_user.route('/users', methods=['GET'])
def get_all():
	"""
	Gets all users in a collection
	"""
    return {"users": repository.get_all_docs("users")}