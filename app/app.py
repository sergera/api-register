from flask import Flask, request
from .controller import user as user_controller
from .data import db

app = Flask(__name__)

database = db.Mongo("mongodb://127.0.0.1:27017","cadastro")

@app.route('/user', methods=['POST'])
def insertUser():
	return user_controller.insert(request.json, database)

@app.route('/', methods=['GET'])
def getUsers():
	return user_controller.getAll(database)

if __name__ == '__main__':
    app.run(debug=True, port=8080) #run app in debug mode on port 5000