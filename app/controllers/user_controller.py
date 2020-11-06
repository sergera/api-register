from flask import Blueprint, request

from app.models.user_model import UserModel
from app.repository import repository

app_user = Blueprint('app_user', __name__)

@app_user.route('/user', methods=['POST'])
def insert():
    """
    Validates and inserts user
    """
    new_user = request.json 
    user = UserModel(new_user)
    user.validate()
    repository.insert_one_key("users", user.to_dict(), {"unique_keys": {"email"}})
    return {"message": "success!"}

@app_user.route('/users', methods=['GET'])
def get_all():
    """
    Gets all users in a collection
    """
    return {"users": repository.get_all_docs("users")}

@app_user.route('/', methods=['GET'])
def root():
    """
    Returns a welcome message
    """
    return {"message": "Welcome to the user registering API! \nUse get('/users') to get all users, and post('/user') to insert a user!"}