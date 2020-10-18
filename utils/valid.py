import requests
import json
import re

def email(address):
	responseFormat = 'json'
	email = address
	response = requests.get(f"https://api.trumail.io/v2/lookups/{responseFormat}?email={email}")
	status = json.loads(response.text)
	return True if (status["validFormat"] and status["hostExists"] and status["deliverable"]) else False

def alphabetic(str):
	regex = re.compile("^[a-zA-Z]+$")
	valid = regex.match(str)
	return valid

def alphabeticSpaced(str):
	regex = re.compile("^((\\ )*[a-zA-Z](\\ )*)+$")
	valid = regex.match(str)
	return valid