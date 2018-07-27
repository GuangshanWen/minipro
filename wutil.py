import os

root = './Images/'

def Generate_ImageID():
	return 0

def Generate_UserID(json_form):
	return json_form["nickname"]


def Insert_Into_DB(json_form):
	return 0

def Mkdir(UserID):
	#root = './Images/'
	path = root+UserID

	isExist = os.path.exists(path)
	
	if not isExist :
		os.makedirs(path)
		print 'mkdir successfully'
		return 0

	return 1
def Check_User(UserID):
	path = root + UserID
	return not os.path.exists(path)
