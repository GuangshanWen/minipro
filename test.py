import requests
import json
import urllib
import urllib2

url = 'http://134.175.178.44:88889'

def test_upload_user_info():
	path = '/upload_user_info'
	myurl = url + path;
	user_info = {'nickname':'wen','gender':'boy','city':'Shenzhen','provice':'Guangdong','county':'China'}
	
		

	r = requests.post(url = myurl,data = user_info)
	#req = urllib2.Request(url = myurl, data = user_info)
	#resp_data = urllib2.urlopen(req);
	#res = resp_data.read()
	
	print r	

def test_upload_image():
	path = '/upload_image'
	myurl = url + path

	data = {'user':'wen'}
	image = {'image':open('./wed.JPG')}
	
	r = requests.post(url = myurl,data = data, files = image)
	print r.content 

def test_append_tags():
	path = '/append_tags'
	myurl = url + path

def test_image_search():
	path = '/search_image'
	myurl  = url + path



if __name__ == '__main__':
	test_upload_user_info()
	test_upload_image()
	test_append_tags()
	test_image_search()
