from flask import request
import json

from controller import getUsers as getUsersController
from controller import insertUser as insertUserController

class Routes:
	def __init__(self, app):
		self.app = app

		@app.route('/', methods=['GET'])
		def getUsers():
			return getUsersController()

		@app.route('/user', methods=['POST'])
		def insertUser():
			data = json.loads(request.data)
			return insertUserController(data)