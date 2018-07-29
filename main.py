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
	print flask.request.headers
       # print flask.request.body.nickName	
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
	
	result = {}
	result['err_code'] = ret
	result['userid'] = UserID
	result = json.dumps(result)	
	#print json_form["nickname"]
	
	return result#5

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
#	print image.filename
 #	print image	
#	image.save('hello.PNG')
 #	print usr_info 
	#print image

 	ImageID = Generate_ImageID()#2
	path = Save_To_ImageDB(UserID,ImageID,image)
#	print path

	err_code,Tags = Get_Images_Tags(path)#3
#	print Tags
	ImageID = image.filename
	#Insert_Into_Tag_Images(UserID,ImageID,Tags)#4
	#Insert_Into_Image_Tags(UserID,ImageID,Tags)#4
	
	result = {}
	if err_code == 0:
		Insert_Into_Tag_Images(UserID,ImageID,Tags)
		Insert_Into_Image_Tags(UserID,ImageID,Tags)
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
@app.route('/tag_search',methods=['POST','GET'])
def tag_earch():
#1. tag = request.get_tag()
#2. user = request.get_user()
#3. images_path_list = get_simi_image(tag)
	userid = flask.request.form('userid')
	tag = flask.request.form('tag')
	image_list = get_simi_img(userid,tag)	
	
	


if __name__ == '__main__':
	app.run(host=addr,port=myport,threaded=False)
