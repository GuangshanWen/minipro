import requests
import json
import threading
import time

sum =0

images = ['test2.jpg','my.jpg','hello.jpg','jietu.JPG']
def test(i):
	url = "http://134.175.178.44:88889/upload_image"
	#header = {'Content-Type': 'multipart/form-data;boundary=adkjh123hk2hk'}
	filepath="C:\\Users\\Administrator\\Desktop\\mini\\"+images[i]
	data = {"user": "wen1"}
	files = {"image": open(filepath, "rb")}
	r = requests.post(url=url, data=data,files=files)
	if r.status_code != 200:
		print ("ERROR")
	respo = r.content.decode()
	print (respo)
#	Json = json.loads(respo)
#	print (Json)


if __name__ == '__main__':
	for i in range(5):
		t =threading.Thread(target=test,args=(i%4,))
		t.start()
