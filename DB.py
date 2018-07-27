from ldb import *
import flask
import leveldb

import os

root = './Metadata/'
Image_tags = 'Image-tags'
Tag_Images = 'Tag-images'
def Create_User_DB(UserID):
	path = root + UserID
	isExist = os.path.exists(path)
	
	if isExist:
		return 1;

	leveldb.LevelDB(path)
	return 0

def Create_Image_Tags_DB(UserID):
	path = root + UserID + Image_tags;
	isExist = os.path.exists(path)
	
	if isExist:
		return 1
	leveldb.LevelDB(path)
	return 0

def Create_Tag_Images(UserID):
	path = root + UserID + Tag_Images
	isExist = os.path.exists(path)

	if isExist :
		return 1

	leveldb.LevelDB(path)

def Get_Image_Tags(json_form):
	return '0asd';

def Insert_Into_User_DB(UserID,json_form):
	pass

def Insert_Into_Tag_Images(json_form,Tags):
	pass

def Insert_Into_Image_Tags(json_form,Tags):
	pass

def Append_Tags_List(Image_Tags_info):
	pass
