from flask import request
import json

from controller import user as userController

class Routes:
	def __init__(self, app):
		self.app = app

		@app.route('/', methods=['GET'])
		def getUsers():
			return userController.getAll()

		@app.route('/user', methods=['POST'])
		def insertUser():
			data = json.loads(request.data)
			return userController.insert(data)