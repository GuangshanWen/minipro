import hashlib
from ldb import *
import flask
import leveldb
import json
import os
import sys
import API
from wutil import *

part_char = '+'

reload(sys)
sys.setdefaultencoding('utf8')

Image_DB = './static/'
root = './Metadata/'
Image_Tags = '-Image-tags'
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
	path = root + UserID + Image_Tags;
	isExist = os.path.exists(path)
	
	if isExist:
		return 1
	leveldb.LevelDB(path)

	lock = open(path+'LOCK','w')
	lock.close()
	return 0

def Create_Tag_Images_DB(UserID):
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
	

def Insert_Into_User_DB(UserID,json_form):
	Dict = json_form.to_dict()
	Json = json.dumps(Dict)
	path = root + UserID
	
	db = leveldb.LevelDB(path)
	db.Put(UserID,Json)	

	return 0

def Append_Image_Tags(UserID,ImageID,Tag):
	if Tag == '':
		return
	path = root + UserID + Image_Tags 

	db = leveldb.LevelDB(path)
	OriginTag = db.Get(ImageID,default='')

	check_list = OriginTag.split(part_char)
	if Tag in check_list:
		return 

	if OriginTag == '':
		OriginTag = Tag
	else :
		OriginTag = OriginTag + part_char + Tag

	db.Put(ImageID,OriginTag)

def Insert_Into_Image_Tag(UserID,ImageID,Tag_list):
	if Tag_list == '':
		return 
	path = root + UserID + Image_Tags  

	db = leveldb.LevelDB(path)
	
	db.Put(ImageID,Tag_list)

#	print OriginTag

def Append_Tag_Images(UserID,ImageID,Tag):
	if Tag == '':
		return
	path = root + UserID + Tag_Images

	db = leveldb.LevelDB(path)
	OriginImageID = db.Get(Tag,default='')

	check_list = OriginImageID.split(part_char)
	if ImageID in check_list:
		return

	if OriginImageID == '':
		OriginImageID = ImageID
	else :
		OriginImageID = OriginImageID + part_char + ImageID
	
	db.Put(Tag,OriginImageID)


def Insert_Into_Tag_Image(UserID,Tag,Image_list):
	if Tag =='':
		return 
	path = root + UserID + Tag_Images
	
	db = leveldb.LevelDB(path)
	
	db.Put(Tag,Image_list)
	

def Append_Tags_List(UserID,ImageID,Tag):
	if Tag =='':
		return 

	Append_Tag_Images(UserID,ImageID,Tag)
	Append_Image_Tags(UserID,ImageID,Tag)
	
def Get_Tags_From_ImageID(UserID,ImageID):
	path = root + UserID + Image_Tags
	db = leveldb.LevelDB(path)
	
	return db.Get(ImageID,default='')

def Delete_Tag_From_List(UserID,ImageID,Tag):
	path = root + UserID +Image_Tags
	db = leveldb.LevelDB(path)	
	Tag_list = db.Get(ImageID,default='')
	if Tag_list == '':
		return 

	Tag_list = Tag_list.split(part_char)
	
	if not Tag in Tag_list:
		return ;
	else:
		Tag_list.pop(Tag_list.index(Tag))

	if not Tag_list:
	#	db = leveldb.LevelDB(path)
		db.Delete(ImageID)
		return

	Tag_list = part_char.join(Tag_list)
	db.Put(ImageID,Tag_list)
	

def Delete_Image_From_List(UserID,ImageID,Tag):
	path = root + UserID + Tag_Images
	db = leveldb.LevelDB(path)	
	Image_list = db.Get(Tag,default = '')

	if Image_list == '':
		return 

	Image_list = Image_list.split(part_char)

	if not ImageID in Image_list:
		return 
	else :
		Image_list.pop(Image_list.index(ImageID))
	
	if not Image_list:
		#db = leveldb.LevelDB(path)
		db.Delete(Tag)
		return 

	Image_list = part_char.join(Image_list)

	db.Put(Tag,Image_list)

def Change_Tag_In_List(UserID,ImageID,NewTag,OldTag):
	if NewTag == '':
		return
	path = root + UserID +Image_Tags
	db = leveldb.LevelDB(path)

	Tag_list = db.Get(ImageID,default='')
	Tag_list  = Tag_list.split(part_char)

	if not OldTag in Tag_list:
		return 
	elif NewTag in Tag_list:
		Tag_list.pop(Tag_list.index(OldTag))
	else:	
		Tag_list[Tag_list.index(OldTag)] = NewTag
	
	Tag_list = part_char.join(Tag_list)
	#Insert_Into_Image_Tag(UserID,ImageID,Tag_list)
	db.Put(ImageID,Tag_list)	

def Get_Tags(UserID,ImageID):
	path = root + UserID + Image_Tags
	db = leveldb.LevelDB(path)

	return db.Get(ImageID,default = '')

def Get_Images(UserID,Tag):
	path = root + UserID + Tag_Images
	db = leveldb.LevelDB(path)

#	print 'Get Images list: ',db.Get(Tag,default = ' ')
	return db.Get(Tag,default = '')

def get_sim_img(userid,Tag):
	path = root + userid + Tag_Images
	db = leveldb.LevelDB(path)
	
	Image_list = db.Get(Tag,default = '')
	return Image_list
#	print Image_list	




	

		 
		
