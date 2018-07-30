import json
#from flask import Flask
#from flask import request
import flask
from wutil import *
from DB import *
from API import *
import hashlib

app = flask.Flask(__name__)

addr = "172.16.0.17"
myport = 88889

@app.route('/upload_user_info',methods=['POST'])
def upload_user_info():
# 1. receive user infomation(json packet)
# 2. generate UserID
# 3. insert user information into redis 
# 4. mkdir ID
# 5. return user ID to client
	#print flask.request.headers
	user_info = flask.request.form
	print user_info
#	print flask.request.headers
       # print flask.request.body.nickName	
	UserID = Generate_UserID(user_info)#2

	print UserID
	Create_User_DB(UserID)
	Create_Image_Tags_DB(UserID)
	Create_Tag_Images(UserID)	
	Create_Unique_CheckDB(UserID)
        
	ret = Insert_Into_User_DB(UserID,user_info)#3
	if ret !=0 :
		pass

	ret = Mkdir(UserID)#4
	if ret != 0 :
		pass
	
	result = {}
	result['err_code'] = ret
	result['userid'] = UserID
	result = json.dumps(result)	
	#print json_form["nickname"]
	
	return result#5
@app.route('/tags_change',methods=['GET','POST'])
def tags_change():
	UserID = flask.request.form['nickName']
	ImageID = flask.request.form['ImageID']
	Old_Tag = flask.request.form['oldtag']
	New_Tag = flask.request.form['newtag']
	tags = Get_Tags(UserID,ImageID)	
	tags = tags.split('+')	
	if Old_Tag in tags:
		tags[tags.index(Old_Tag)] = New_Tag
	else :
		return 'done'
#1 
	Tag = ''
	for tag in tags:
		Tag = Tag + '+' + tag			
	Tag = [Tag]
	Insert_Into_Image_Tags(UserID,ImageID,Tag)
	
#2.
	Image_list = Get_Images(UserID,Old_Tag)
	Image_list = Image_list.split('+')
	Image_list.pop(Image_list.index(ImageID))
	
	Old_Tag = [Old_Tag]
	if not Image_list:
		Delete_Tag_Images(UserID,Old_Tag)	
	
	else :
		Img = ''
		for img in Image_list:
			Img = Img + '+' + img			

#3.	 	
 	Insert_Into_Tag_Images(UserID,ImageID,New_Tag)
	print tags
	return 'done'

@app.route('/tag_delete',methods=['GET','POST'])
def tag_delete():
	ImageID = flask.request.form['ImageID']
	UserID = flask.request.form['nickName']

	Tag = flask.request.form['tag']

	Image_list = Get_Images(UserID,Tag)
	Image_list = Image_list.split('+')
	if not ImageID in Image_list:
		return 'done'

#1. 
	Image_list.pop(Image_list.index(ImageID))
	Img = ''
	for img in Image_list:
		Img = Img + '+' + img			
	
	Tag = {Tag}
	Insert_Into_Tag_Images(UserID,ImageID,Tag)	

#2.	
	Tags =	Get_Tags(UserID,ImageID)
	Tags = Tags.split('+')

	if not Tag in Tags:
		return 'done'

	Tags.pop(Tags.index(Tag))			
	if not Tags:
		Delete_Image_Tags(UserID,ImageID)
		return 'done'
	
	Tag = ''
	for tag in Tags:
		Tag = Tag + '+' + tag

	Insert_Into_Image_Tags(UserID,ImageID,[Tag])

	return 'done'

@app.route('/upload_image',methods=['GET','POST'])
def upload_image():
# 1. receive image
# 2. generate ImageID
# 3. call back-API to get image tags  
# 4. insert new image-tags to redis
#	print flask.request.get_data()	
#	print flask.request.headers
	UserID = flask.request.form['nickName']
	#print type(flask.request.files['image'])
	
	ret = Check_User(UserID)
	#ret = 0
	if ret == 1:
		result = {}
		result['err_code'] = 1
		result['err_msg'] = 'user not found'
		return json.dumps(result)	

	image = flask.request.files.get('image')#1
#	print type(hashlib.md5(image.read()).hexdigest())
#	print image.read()
#	print image.filename
 #	print image	
#	image.save('hello.PNG')
 #	print usr_info 
	#print image

 #	ImageID = Generate_ImageID()#2
	Flag,ImageID,path = Save_To_ImageDB(UserID,image)
#	print path
	print path	
	if Flag == True:
		err_code,Tags = Get_Images_Tags(path)#3
		print 'from raw:',Tags
	else :
		err_code = 0
		Tags = Get_Tags(UserID,ImageID)
		Tags = Tags.split('+')
		print('tags from db:',Tags)
#	print Tags
#	ImageID = image.filename
	#Insert_Into_Tag_Images(UserID,ImageID,Tags)#4
	#Insert_Into_Image_Tags(UserID,ImageID,Tags)#4
	
	result = {}
	if err_code == 0 and Flag == True:
		Insert_Into_Tag_Images(UserID,ImageID,Tags)
		Insert_Into_Image_Tags(UserID,ImageID,Tags)
		result['Tags'] = Tags
		result['Imageid'] = ImageID
	elif Flag == False:
		result['Tags'] = Tags
		result['Imageid'] = ImageID
	else :
		result['Imageid'] = ImageID
		result['err_msg'] = Tags
	
	result['err_code'] = err_code
	result = json.dumps(result)

	return result

@app.route('/append_tags',methods=['POST'])
def append_tags():
#1. receive image-tags
#2. append coressponding tags-list
	ImageID = flask.request.form['ImageID']	
	UserID = flask.request.form['nickName']
	tagtmp = flask.request.form['tag']
	tag = {tagtmp}
	#print ('in append_tags funtion :', Get_Tags(UserID,ImageID))
	ret = Append_Tags_List(UserID,ImageID,tag)
	print Get_Images(UserID,tagtmp)	
	print Get_Tags(UserID,ImageID)
	return Get_Tags(UserID,ImageID)

@app.route('/search_image',methods=['POST','GET'])
def search_image():
#1. receive image(decode)
#2. call back-end API to get result sorted image list(url list)
#3. send to client 
#	Image = request.get_data()
#	Image_list = Search_Image(Image,userpath)
#       send(client...)

	return 'image list'
@app.route('/tag_search',methods=['POST','GET'])
def tag_search():
#1. tag = request.get_tag()
#2. user = request.get_user()
#3. images_path_list = get_simi_image(tag)
	print flask.request.form
	print flask.request
	userid = flask.request.form['nickName']
	tag = flask.request.form['tag']
	
	#print userid,tag
		
	
	return Get_Images(userid,tag)
 		

if __name__ == '__main__':
	app.run(host=addr,port=myport,threaded=False)
