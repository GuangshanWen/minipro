import requests
import json
import threading
import time

sum =0
url = "http://134.175.178.44:88889"
images = ['test2.jpg','my.jpg','hello.jpg','jietu.JPG']
def test_upload_image(i):
	url = "http://134.175.178.44:88889/upload_image"
	#header = {'Content-Type': 'multipart/form-data;boundary=adkjh123hk2hk'}
	filepath="C:\\Users\\Administrator\\Desktop\\mini\\"+images[i]
	data = {"user": "guangshan"}
	files = {"image": open(filepath, "rb")}
	r = requests.post(url=url, data=data,files=files)
	if r.status_code != 200:
		print ("ERROR")
	respo = r.content.decode()
	print (respo)
#	Json = json.loads(respo)
#	print (Json)

def test_upload_user_info():
	path = '/upload_user_info'
	myurl = url + path;
	user_info = {'nickname':'guangshan','gender':'boy','city':'Shenzhen','provice':'Guangdong','county':'China'}
	
		

	r = requests.post(url = myurl,data = user_info)
	#req = urllib2.Request(url = myurl, data = user_info)
	#resp_data = urllib2.urlopen(req);
	#res = resp_data.read()
	
	print (r.content.decode())	

if __name__ == '__main__':
	#for i in range(9):
	test_upload_user_info()
	test_upload_image(1)
		#t =threading.Thread(target=test_upload_image,args=(i%4,))
		#t.start()
