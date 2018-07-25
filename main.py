import json
from flask import Flask
from flask import request

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
	print user_info
	return 'err'

@app.route('/upload_image',methods=['POST'])
def upload_image():
# 1. receive image
# 2. generate ImageID
# 3. call back-API to get image tags  
# 4. insert new image-tags to redis
	pass

@app.route('/append_tags',methods=['POST'])
def append_tags():
#1. receive image-tags
#2. append coressponding tags-list

	pass

@app.route('/search_image',methods=['POST','GET'])
def search_image():
#1. receive image(decode)
#2. call back-end API to get result sorted image list(url list)
#3. send to client 
	pass

if __name__ == '__main__':
	app.run(host=addr,port=myport)
