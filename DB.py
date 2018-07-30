import hashlib
from ldb import *
import flask
import leveldb
import json
import os
import sys
import API
from wutil import *

reload(sys)
sys.setdefaultencoding('utf8')

Image_DB = './static/'
root = './Metadata/'
Image_tags = '-Image-tags'
Tag_Images = '-Tag-images'
Unique_Check_DB = '-UniqueCheck'

def Create_Unique_CheckDB(UserID):
	path = root + UserID + Unique_Check_DB;
	leveldb.LevelDB(path)

	return 0

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

	lock = open(path+'LOCK','w')
	lock.close()
	return 0

def Create_Tag_Images(UserID):
	path = root + UserID + Tag_Images
	isExist = os.path.exists(path)

	if isExist :
		return 1
	
	leveldb.LevelDB(path)

	lock = open(path+'-LOCK','w')
	lock.close()

	return 0

def Save_To_ImageDB(UserID,Image):
	path = root + UserID + Unique_Check_DB
	content = Image.read()
	Hash = hashlib.md5(content).hexdigest()
	db = leveldb.LevelDB(path)
	
	ImageID = db.Get(Hash,default = ' ')
	if ImageID != ' ':
		return False,ImageID,Image_DB + UserID + '/' + ImageID
	
	ImageID = Image.filename
	db.Put(Hash,ImageID)
	#extension = Get_Extension(Image.filename)
	
	path = Image_DB + UserID + '/' + ImageID
	#path = Image_DB + UserID + '/' + ImageID + '.' + extension
	fil = open(path,'w')
	#print content
	fil.write(content)
	fil.close()
	return True,ImageID,path
	
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
	OriginTag = db.Get(ImageID,default=' ')
        	
	
	for i in Tags:
		tag_list = OriginTag.split('+')
		if i in tag_list:
			continue

	#	print 'tagssss: ',i
		if OriginTag == ' ':
			OriginTag = i
		else : 
			OriginTag = OriginTag + '+' + i	
	print ('insert in to image tags: ',OriginTag)
	db.Put(ImageID,OriginTag)

#	print OriginTag

def Insert_Into_Tag_Images(UserID,ImageID,Tags):
	path = root + UserID + Tag_Images
	
	db = leveldb.LevelDB(path)
	for tag in Tags:
		OriginImgID = db.Get(tag,default=' ')
		
		image_list = OriginImgID.split('+')
		if ImageID in image_list:
			continue

		if OriginImgID == ' ':
			OriginImgID = ImageID
		else:
			OriginImgID = OriginImgID + '+'  + ImageID
		db.Put(tag,OriginImgID)
	
	
	return 0	

def Append_Tags_List(UserID,ImageID,tag):
	#path_tag_images = root + UserID + Tag_Images
	#path_image_tags = root + UserID + Image_tags

	Insert_Into_Tag_Images(UserID,ImageID,tag)
	Insert_Into_Image_Tags(UserID,ImageID,tag)
	
def Get_Tags(UserID,ImageID):
	path = root + UserID + Image_tags
	db = leveldb.LevelDB(path)
	
	#print 'gettags::',db.Get(ImageID)
	return db.Get(ImageID,default=' ')

def Delete_Tag_Images(UserID,tag):
	path = root + UserID +Tag_Images
	db = leveldb.LevelDB(path)
	
	tag = tag[0]
	db.Delete(tag)

def Delete_Image_Tags(UseID,ImageID):
	path = root + UserID +Image_tag
	db = leveldb.LevelDB(path)

	db.Delete(ImageID)

def Get_Images(UserID,Tag):
	path = root + UserID + Tag_Images
	db = leveldb.LevelDB(path)

	print 'Get Images list: ',db.Get(Tag,default = ' ')
	return db.Get(Tag,default = ' ')

def get_sim_img(userid,tag):
	path = root + userid + Tag_Images
	db = leveldb.LevelDB(path)
	
	Image_list = db.Get(tag,default = 'null')
#	print Image_list	




	

		 
		
