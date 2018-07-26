import requests
import json
import urllib
import urllib2

url = 'http://134.175.178.44:8888/upload_user_info'

def test_upload_user_info():
	user_info = '{"nickname":"fuckbug","gender":"boy","city":"Shenzhen","provice":"Guangdong","county":"China"}'
	
	req = urllib2.Request(url = url, data = user_info)
	resp_data = urllib2.urlopen(req);
	res = resp_data.read()

	print res	

def test_upload_image():
	pass

def test_upload_tags():
	pass

def test_image_search():
	pass
