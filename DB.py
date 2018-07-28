from ldb import *
import flask
import leveldb
import json
import os

Image_DB = './Images/'
root = './Metadata/'
Image_tags = '-Image-tags'
Tag_Images = '-Tag-images'
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

def Save_To_ImageDB(UserID,ImageID,Image):
	path = Image_DB + UserID + '/' + ImageID + '.PNG'
	Image.save(path)
	return 0
	
def Get_Image_Tags(json_form):
	return '0asd';

def Insert_Into_User_DB(UserID,json_form):
	Dict = json_form.to_dict()
	Json = json.dumps(Dict)
	path = root + UserID
	
	db = leveldb.LevelDB(path)
	db.Put(UserID,Json)	

	return 0

def Insert_Into_Image_Tags(UserID,ImageID,Tags):
	path = root + UserID + Image_tags  

	db = leveldb.LevelDB(path)
	OriginTag = db.Get(ImageID,default='')
	
	for i in Tags:
		OriginTag = '\n' + i	

	db.Put(ImageID,OriginTag)

	print OriginTag

def Insert_Into_Tag_Images(UserID,ImageID,Tags):
	path = root + UserID + Tag_Images
	
	db = leveldb.LevelDB(path)
	for tag in Tags:
		OriginImgID = db.Get(tag,default='')
		OriginImgID = OriginImgID + '\n'  + ImageID
		db.Put(tag,OriginImgID)
	
	return 0	

def Append_Tags_List(UserID,ImageID,Image):
	#path_tag_images = root + UserID + Tag_Images
	#path_image_tags = root + UserID + Image_tags

	Insert_Into_Tag_Images(UserID,ImageID,Image)
	Insert_Into_Image_Tags(UserID,ImageID,Image)
	



	
