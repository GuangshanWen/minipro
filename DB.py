import chardet 
import hashlib
import random
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
count_db = 'count_db'
Global_dir = 'global_image'
Global_metadata = 'global_metadata'


def Save_To_Local(UserID,ImageID,content):
	#save global image to local user
	#first check if the image exist
	#then save
	#how about global tags?
	path = root + UserID + Unique_Check_DB

	Hash = hashlib.md5(content).hexdigest()
	db = leveldb.LevelDB(path)

	imageid = db.Get(Hash,default = ' ')
	if imageid == ' ':
		db.Put(Hash,ImageID)
		path = Image_DB + UserID + '/' + ImageID

		fil = open(path,'w')
		#print content
		fil.write(content)
		fil.close()

		return ImageID
	
	return imageid

	

def Create_Globalmetadata():
	path = Image_DB + Global_metadata + '/' + 'global'
	
	isexist = os.path.exists(path)
	if isexist:
		return 1

	leveldb.LevelDB(path)

	return 0
	

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

def Get_Fresh_Images(UserID,files,count,page):
	count = int(count)	
	page = int(page)
	path = root + UserID + count_db
	db = leveldb.LevelDB(path)
	#print files	
	if int(page)  == 1:
		random.shuffle(files)
	#	print files
		db.Put('page',part_char.join(files))
	image_list = db.Get('page',default = '')
	image_list = image_list.split(part_char)
	print 'count!!!! ',count
	print 'imagelist:!!!',len(image_list)
	if len(image_list) < (count) :
		count = len(image_list)
	print 'count!!!',count	
	result = []
	n = 0
	#print 'image_list!!! ',image_list
	for i in image_list:
	#	print 'i!!!! ',i
		result.append(i)
	#	image_list.pop(image_list.index(i))	
		n = n+1
		if n == count:
			break	
	for i in result:
		image_list.pop(image_list.index(i))
	#print 'result!!!',result
	db.Put('page',part_char.join(image_list))
	return result#list


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
	
	db_path = Image_DB + Global_metadata + '/' +'unique_global'
	globaldb = leveldb.LevelDB(db_path)
	flag = globaldb.Get(Hash,default='')
	if flag == '':
		global_path = Image_DB + Global_dir+ '/' +ImageID
		print'save in to globa imagedb: ', global_path
		fil = open(global_path,'w')
		fil.write(content)
		fil.close()

		globaldb.Put(Hash,ImageID)

		#globaltag = Image_DB + Global_metadata + '/' +' global'
	#	value = {'Tags':{}}
	#	value = json.dumps(value)
	#	globaldb.Put(Hash,value)		
	
	return True,ImageID,path
def Get_Global_Tag(ImageID):
	path = Image_DB + Global_metadata + '/' + 'global'
	db = leveldb.LevelDB(path)

	value = db.Get(ImageID,default = '')
	print 'global tags:',value
	return value

def Insert_Into_Globaldb(ImageID,Tag):
	path = Image_DB +Global_metadata + '/' + 'global'
	db = leveldb.LevelDB(path)

	value = db.Get(ImageID,default = '')
	print 'tag: ',Tag
	Tag = Tag.decode('utf8')
	if value == '':
		print 'default'
		value = {}
		value[Tag] = str(1)
	else :
		print 'get global tags: ',value
		value = json.loads(value)
	 	print 'value type: ',type(value)	
		#Tag = Tag.encode('utf8')
		print 'value: ',value
		# Tag.decode('utf8')
		if Tag in value:
			print 'add 1 !!!!'
			value[Tag] = str(int(value[Tag]) + 1)
		else :
			print 'init 1!!!!'
			value[Tag] = str(1)
	print 'insert in to global db : ',(json.dumps(value))
	db.Put(ImageID,json.dumps(value))
	print 'get global tag: ',db.Get(ImageID)
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
	
	if Tag == '':#return all images
		path = Image_DB + UserID
		files = os.listdir(path)
		result = part_char.join(files)

		return result

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




	

		 
		
