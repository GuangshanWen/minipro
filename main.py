import json
from flask import Flask
from flask import request
from wutil import *
from DB import *
from API import *

app = Flask(__name__)

addr = "172.16.0.17"
myport = 8888

@app.route('/upload_user_info',methods=['POST'])
def upload_user_info():
# 1. receive user infomation(json packet)
# 2. generate UserID
# 3. insert user information into redis 
# 4. mkdir ID
# 5. return user ID to client
	user_info = request.get_data()
	json_form = json.loads(user_info)#1

	UserID = Generate_UserID(json_form)#2
        
	ret = Insert_Into_User_DB(UserID,json_form)#3
	if ret !=0 :
		pass

	ret = Mkdir(UserID)#4
	if ret != 0 :
		pass
	
	#print json_form["nickname"]
	return UserID#5

@app.route('/upload_image',methods=['POST'])
def upload_image():
# 1. receive image
# 2. generate ImageID
# 3. call back-API to get image tags  
# 4. insert new image-tags to redis
	img_info = request.get_data()
	json_form = json.loads(user_info)#1

 	ImageID = Generate_ImageID()#2
	Tags = Get_ImageTags(json_form)#3

	Insert_Into_Tag_Images(json_form,Tags)#4
	Insert_Into_Image_Tags(json_form,Tags)#4

	return Tags
@app.route('/append_tags',methods=['POST'])
def append_tags():
#1. receive image-tags
#2. append coressponding tags-list

	Image_Tags_info = request.get_data()
	ret = Append_Tags_List(Image_Tags_info)

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
