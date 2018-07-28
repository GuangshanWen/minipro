#-*-coding=utf-8 -*-
import json
#from flask import Flask
#from flask import request
import flask
from wutil import *
from DB import *
from API import *

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
	#print user_info	

	UserID = Generate_UserID(user_info)#2
	print UserID
	Create_User_DB(UserID)
	Create_Image_Tags_DB(UserID)
	Create_Tag_Images(UserID)	
        
	ret = Insert_Into_User_DB(UserID,user_info)#3
	if ret !=0 :
		pass

	ret = Mkdir(UserID)#4
	if ret != 0 :
		pass
	
	#print json_form["nickname"]
	return UserID#5

@app.route('/upload_image',methods=['GET','POST'])
def upload_image():
# 1. receive image
# 2. generate ImageID
# 3. call back-API to get image tags  
# 4. insert new image-tags to redis
#	print flask.request.get_data()	
	print flask.request.headers
	UserID = flask.request.form['user']
	#print type(flask.request.files['image'])
	
	ret = Check_User(UserID)
	ret = 0
	if ret == 1:
		return 'unsafe user'	

	image = flask.request.files.get('image')#1
#	print image.filename
 #	print image	
#	image.save('hello.PNG')
 #	print usr_info 
	#print image

 	ImageID = Generate_ImageID()#2
	path = Save_To_ImageDB(UserID,ImageID,image)
	print path

	Tags = Get_Images_Tags(path)#3
	print Tags
	ImageID = image.filename
	Insert_Into_Tag_Images(UserID,ImageID,Tags)#4
	Insert_Into_Image_Tags(UserID,ImageID,Tags)#4

	result = {ImageID:Tags}
	result = json.dumps(result)

	return result

@app.route('/append_tags',methods=['POST'])
def append_tags():
#1. receive image-tags
#2. append coressponding tags-list

	Image_Tags_info = request.get_data()
	ret = Append_Tags_List(UserID,ImageID,Image)

	return 'done'

@app.route('/search_image',methods=['POST','GET'])
def search_image():
#1. receive image(decode)
#2. call back-end API to get result sorted image list(url list)
#3. send to client 
	Image = request.get_data()
	Image_list = Search_Image(Image)

	return 'image list'


if __name__ == '__main__':
	app.run(host=addr,port=myport)
