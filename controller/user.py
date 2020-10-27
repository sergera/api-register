from model.user import User

"""

The controller

On Insert:
1- creates the model, 
2- validates the input, 
3- and passes the model to the data layer.

On Get:
1- passes the collection name to the data layer.

"""

def insert(new_user, database):
	user = User(new_user)
	valid_email = user.validateEmail()
	valid_name = user.validateName()
		
	if not valid_email:
		return "Invalid email!"
	elif not valid_name:
		return "Invalid name!"
	else:
		user_dict = user.__dict__
		return database.insertOneKey("users", user_dict, {"unique_keys": {"email"}})

def getAll(database):
	return {"users": database.getAllDocs("users")}