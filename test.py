#-*-coding=utf-8 -*-
import requests
import json
import urllib
import urllib2
import sys

url = 'http://134.175.178.44:88889'
#sys.setdefaultencoding('utf8')
def test_upload_user_info():
	path = '/upload_user_info'
	myurl = url + path;
	user_info = {'nickName':'wen','gender':'boy','city':'Shenzhen','provice':'Guangdong','country':'China'}
	
		

	r = requests.post(url = myurl,data = user_info)
	#req = urllib2.Request(url = myurl, data = user_info)
	#resp_data = urllib2.urlopen(req);
	#res = resp_data.read()
	
	print r	

def test_upload_image():
	path = '/upload_image'
	myurl = url + path

	data = {'nickName':'wen'}
	image = {'image':open('./test.jpg')}
	
	r = requests.post(url = myurl,data = data, files = image)
	resp =  r.content.decode()
	print resp
	#Json = json.loads(resp)
	#print Json

def test_append_tags():
	path = '/append_tags'
	myurl = url + path
	
	data = {'nickName':'wen','tag':'guangshan','ImageID':'test.jpg'}	
	r = requests.post(url = myurl,data = data)	
	
	print r.content

def test_image_search():
	path = '/search_image'
	myurl  = url + path

def test_tag_search():
	path = '/tag_search'
	myurl = url + path

	data = {'nickName':'wen','tag':'guangshan'}

	r = requests.post(url = myurl,data = data)
	
	print r.content

if __name__ == '__main__':
	test_upload_user_info()
	test_upload_image()
	test_append_tags()
	test_image_search()
	test_tag_search()
