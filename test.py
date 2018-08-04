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
	user_info = {'nickName':'guangshan','gender':'boy','city':'Shenzhen','provice':'Guangdong','country':'China'}
	
		

	r = requests.post(url = myurl,data = user_info)
	#req = urllib2.Request(url = myurl, data = user_info)
	#resp_data = urllib2.urlopen(req);
	#res = resp_data.read()
	
	print 'test_upload_user_info:',r.content	

def test_collect_image():
	path = '/collect_image'
	myurl = url+path
	
	data = {'nickName':'wen','ImageID':'hello.PNG'}
	r = requests.post(url = myurl,data = data)

	print r.content
def test_recommended_image():
	path = '/recommended_image'
	myurl = url + path
	data = {'nickName':'wen','count':100,'page':1}
	
	r = requests.post(url = myurl,data = data)
	print r.content

def test_upload_image():
	path = '/upload_image'
	myurl = url + path

	data = {'nickName':'guangshan'}
	image = {'image':open('./hello.PNG')}
	
	r = requests.post(url = myurl,data = data, files = image)
	resp =  r.content.decode()
	print 'test image upload: ',resp
	#Json = json.loads(resp)
	#print Json

def test_append_tags():
	path = '/append_tags'
	myurl = url + path
	
	data = {'nickName':'wen','tag':'wenwen','ImageID':'test.jpg'}	
	r = requests.post(url = myurl,data = data)	
	
	print 'test append tags:',r.content

def test_image_search():
	path = '/search_image'
	myurl  = url + path
	
	data = {'nickName':'wen'}
	files = {'image':open('./test.jpg')}	

def test_tag_search():
	path = '/tag_search'
	myurl = url + path

	data = {'nickName':'wen','tag':''}

	r = requests.post(url = myurl,data = data)
	
	print 'test tag search: ',r.content

def test_tag_change():
	path = '/tags_change'
	myurl = url + path

	data = {'nickName':'wen','oldtag':'wenwen','ImageID':'test.jpg','newtag':'惹不起'}
	r = requests.post(url = myurl,data = data)

	print 'test tag change :' , r.content

def test_tag_delete():
	path = '/tag_delete'
	myurl = url + path

	data = {'nickName':'wen','ImageID':'test.jpg','tag':'wenwen'}
	r = requests.post(url = myurl,data = data)

	print r.content

if __name__ == '__main__':
#	img = open('./test.jpg')
#	print img.read()
	test_upload_user_info()
	test_upload_image()
	test_append_tags()
#	test_image_search()
	test_tag_search()
	test_collect_image()
#	test_tag_change()
	test_recommended_image()
#	test_tag_delete()
