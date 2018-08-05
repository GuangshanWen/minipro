import wutil
import sys
import jieba
sys.path.append('./aip')
from ocr import *
import time

blur_flag = True
def jie_ba(string):
	cut = jieba.cut_for_search(string)
	strings = ','.join(cut)

	strings = string + ',' + strings
	result = []
	
	ss =  strings.split(',')
	for i in ss:
		if len(ss) >= 1:
			result.append(i)	
	return result
def get_bytes_for_image(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

def image_path_ocr(image_path):
    #print image_path
    appId = '11594330'
    apiKey = 'FnN8cbzZcELlGqdl4MNYPam2'
    secretKey = 'trXCt8yAzTzCfOQxELuQC9N4N19NR6GW'
    time.sleep(0.3)
    engine = AipOcr(appId, apiKey, secretKey)
    result = engine.basicGeneral(get_bytes_for_image(image_path))
    #print result
    err_code = 0
    results = []
    
    if not u'words_result' in result:
	err_code = 1
	results.append(result[u'error_msg'])
	return err_code,results
    #results = []
    
    for wr in result['words_result']:
        results.append(wr['words'].encode('utf-8'))
    
    result = ''
    for wr in results:
	if len(wr)>= 1:
		result = result + wr

    if blur_flag == False:
	results = [result]
    else :
	results = jie_ba(result)
    return err_code,results

#if __name__ == '__main__':
#    results = image_path_ocr('test2.jpg')
#    for r in results:
#        print(r)


def Get_Images_Tags(path):
	#return {wutil.Get_Random_Str(6)}
	return image_path_ocr(path)
	

def Search_Image(Image):
	return 'wtf'
