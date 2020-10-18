#returns string trimmed and with all space series reduced for 1 space
def name(str):
	stringList = str.split(" ")
	noSpaceList = [string for string in stringList if string is not ""]
	space = " "
	formattedName = space.join(noSpaceList)
	return formattedName.lower()

#receives a list of error strings and returns an error string with spaces and error numbers
def error(errorList):
	error = 'Error! '
	for string in errorList:
		error = error + f"#{errorList.index(string)} " + string + " "
	return error
