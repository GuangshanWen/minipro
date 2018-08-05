import operator
import jieba
import json
import flask
from wutil import *
from DB import *
from API import *
import hashlib
from search_image.main import search_similar_pics
import os
import random
import common

app = flask.Flask(__name__)

addr = "172.16.0.17"
myport = 23353


global __ImageID__,__NickName__,__ErrCode__,__UserID__,__OldTag__,__NewTag__,__ErrMsg__,__Image__,__Tag__,__ResultImg__,__ResultImage__,__TagList__

__ImageID__ = 'ImageID'
__NickName__ = 'nickName'
__ErrCode__ = 'err_code'
__UserID__ = 'userid'
__OldTag__ = 'oldtag'
__NewTag__ = 'newtag'
__ErrMsg__ = 'err_msg'


__Image__ = 'image'
__Tag__ = 'tag'


__ResultImg__ = 'image_result'
__TagList__ = 'Tags'

__ResultImage__ = 'Imageid'



@app.route('/deblured_image',methods = ['POST','GET'])
def deblured_image():
	pass

@app.route('/collect_image',methods=['POST','GET'])
def collect_image():
	ImageID = flask.request.form[__ImageID__]
	UserID = flask.request.form[__NickName__]
	
	global_tags  = Get_Global_Tag(ImageID)

	global_dir = './static/global_image/'
	image = global_dir + ImageID
 
	isExist = os.path.exists(image)
	if not isExist:
		return 'exist'
	
	img = open(image)
	content = img.read()
	ImageID = Save_To_Local(UserID,ImageID,content) # save to local dir
	Increase_Hot_Image(ImageID)		

	Tags = json.loads(global_tags)
	Tags = Tags.keys()
	Tags = Tags[0]
	Tags = jie_ba(Tags)
	for tag in Tags:
		Append_Tags_List(UserID,ImageID,tag)
	
	return ImageID

@app.route('/hot_collect',methods=['POST','GET'])
def hot_collect():
	global_dir = './static/global_image/'
	#files = os.listdir(global_dir)
	count = flask.request.form['count']
	page = flask.request.form['page']
	page = int(page)
	count = int(count)
	
	files = os.listdir(global_dir)
	
	
	print 'files~~~~ ',files	
	result = {}
	for f in files:
		#Tags = Get_Global_Tag(f)
		Times = Get_Collect_Time(f)
	#	print 'Tags in hot collect: ',Tags
		if Times != '':
			result[f] = int(Times)
		else:
			result[f] = 0
	
	sorted_x = sorted(result.items(),key=operator.itemgetter(1))
	print 'sorted~~~~ ',sorted_x
	result = {}
	for i in sorted_x:
		f = i[0]
		t = i[1]		
			
		Tag = Get_Global_Tag(f)
		print 'Tag ~~~ ',Tag

		if Tag == '':
			Tag = {"NULL":"0"}
			Tag = json.dumps(Tag)
			#print "Tag!!!!!!: ",Tag
		#print 'Tag: ~~~~ ',Tag
		Tag = json.loads(Tag)
		keys = list(Tag.keys())		
		result[f] = {keys[0]:str(t)}	
	result_image = {}
	result_image['image_result'] = result
	result_image['err_code'] = 0

	return json.dumps(result_image)	

@app.route('/recommended_image',methods=['POST','GET'])
def recommended_image():
	user_info = flask.request.form[__NickName__]
	count = flask.request.form['count'] #client +1
	page = flask.request.form['page']
	global_dir = './static/global_image/'
		
	files = os.listdir(global_dir)
	
	n = page
	#subset = random.sample(files,n)
	print 'files:',files
	subset = Get_Fresh_Images(user_info,files,count,page)
	print'subset:: ', subset
	image_list = {}
	for i in subset:
		#image_list[i] = Get_Global_Tag(i)	
		val = Get_Global_Tag(i)
		if val != '':
			image_list[i] = val
	print image_list
	result = {}
	result[__ResultImg__] = image_list
	#result[__ResultImg__] = ','.join(subset)
	result[__ErrCode__] = 0
	result['page'] = n
	return json.dumps(result)

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
	Create_Tag_Images_DB(UserID)	
	Create_Unique_CheckDB(UserID)
	Create_Globalmetadata()
        
	ret = Insert_Into_User_DB(UserID,user_info)#3
	if ret !=0 :
		pass

	ret = Mkdir(UserID)#4
	if ret != 0 :
		pass
	
	result = {}
	result[__ErrCode__] = ret
	result[__UserID__] = UserID
	result = json.dumps(result)	
	#print json_form["nickname"]
	
	return result#5
@app.route('/tags_change',methods=['GET','POST'])
def tags_change():
	UserID = flask.request.form[__NickName__]
	ImageID = flask.request.form[__ImageID__]
	OldTag = flask.request.form[__OldTag__]
	NewTag = flask.request.form[__NewTag__]


	print 'before change Tag list: ',Get_Tags(UserID,ImageID)
	print 'before change Image list of Old Tag', Get_Images(UserID,OldTag)
	print 'before change Image list of New Tag', Get_Images(UserID,NewTag)
	Change_Tag_In_List(UserID,ImageID,NewTag,OldTag)

	
	Delete_Image_From_List(UserID,ImageID,OldTag)

	
	Append_Tag_Images(UserID,ImageID,NewTag)

	print 'after change Tag list: ',Get_Tags(UserID,ImageID)
	print 'after change Image list of old tag', Get_Images(UserID,OldTag)
	print 'after change image list of new tag',Get_Images(UserID,NewTag)

	return Get_Tags(UserID,ImageID)

@app.route('/tag_delete',methods=['GET','POST'])
def tag_delete():
	ImageID = flask.request.form[__ImageID__]
	UserID = flask.request.form[__NickName__]

	Tag = flask.request.form[__Tag__]

	print 'before delete Tag list: ',Get_Tags(UserID,ImageID)
	print 'before delete Image list', Get_Images(UserID,Tag)

	
	Delete_Tag_From_List(UserID,ImageID,Tag)


	Delete_Image_From_List(UserID,ImageID,Tag)

	print 'after delete Tag list: ',Get_Tags(UserID,ImageID)
	print 'after delete Image list', Get_Images(UserID,Tag)

	return Get_Tags(UserID,ImageID)

@app.route('/upload_image',methods=['GET','POST'])
def upload_image():
	UserID = flask.request.form[__NickName__]
	ret = Check_User(UserID)
	#ret = 0
	if ret == 1: 
		result = {}
		result[__ErrCode__] = 1
		result[__ErrMsg__] = 'user not found'
		return json.dumps(result)	


	image = flask.request.files.get(__Image__)#1
	Flag,ImageID,path = Save_To_ImageDB(UserID,image) 
	
	app.logger.info('hello world')	
	err_code,Tags = Get_Images_Tags(path)

	
	if err_code == 0:
		for tag in Tags:
			print tag
			Append_Tags_List(UserID,ImageID,tag)
	Insert_Into_Globaldb(ImageID,Tags[0])
			
	result = {}
	if err_code == 0 : #API
		result[__TagList__] = [Tags[0]]
		result[__ResultImage__] = ImageID
	else : #API
		result[__ResultImage__] = ImageID
		result[__ErrMsg__] = Tags
	
	result[__ErrCode__] = err_code
	result = json.dumps(result)

	return result

@app.route('/append_tags',methods=['POST'])
def append_tags():
#1. receive image-tags
#2. append coressponding tags-list
	ImageID = flask.request.form[__ImageID__]	
	UserID = flask.request.form[__NickName__]
	tag = flask.request.form[__Tag__]
	print 'in append tag'
	#print ('in append_tags funtion :', Get_Tags(UserID,ImageID))
	ret = Append_Tags_List(UserID,ImageID,tag)
	#Insert_Into_Globaldb(ImageID,tag)	
	print Get_Images(UserID,tag)	
	print Get_Tags(UserID,ImageID)
	return Get_Tags(UserID,ImageID)

@app.route('/search_image',methods=['POST','GET'])
def search_image():
#1. receive image(decode)
#2. call back-end API to get result sorted image list(url list)
#3. send to client 
	UserID = flask.request.form[__NickName__]
        ret = Check_User(UserID)
        
	result = {}
	if ret == 1:
        #        result = {}
                result[__ErrCode__] = 1
                result[__ErrMsg__] = 'user not found'
		result[__ResultImg__] = ""
                return json.dumps(result)
	else:
		result[__ErrCode__] = 0

        image = flask.request.files.get('image');
        image.save("temp/"+image.filename);
        query_img="temp/"+image.filename;
        #dst_dir="static/"+;
        dst_dir="static/global_image/"
        result_image_list = search_similar_pics(query_img, dst_dir);

#print(result_image_list);
        tmp="";
        #for r_image in result_image_list:
         #       tmp=tmp+r_image+",";
        if len(result_image_list) != 0:
		result[__ErrCode__] = 0
		result[__ResultImg__] = ','.join(result_image_list)
	else :
		result[__ErrCode__] = 1
		result[__ResultImg__] = tmp
	
	return json.dumps(result)


@app.route('/tag_search',methods=['POST','GET'])
def tag_search():
#1. tag = request.get_tag()
#2. user = request.get_user()
#3. images_path_list = get_simi_image(tag)
	print flask.request.form
	print flask.request
	userid = flask.request.form[__NickName__]
	tag = flask.request.form[__Tag__]
	
	print userid,tag
		
	result = {}
	image_list = Get_Images(userid,tag)
	if len(image_list):
		result[__ResultImg__] = ','.join(image_list.split(part_char))
		result[__ErrCode__] = 0
 	else:
		result[__ResultImg__] = ''
		result[__ErrCode__] = 1

	return json.dumps(result)

if __name__ == '__main__':
#	app.run(host=addr,port=myport,threaded=False)
	app.run(host=addr,port=myport,threaded=False,ssl_context=('../doutu.crt','../doutu.key'))
