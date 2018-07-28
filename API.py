import wutil
import sys
sys.path.append('./aip')
import ocr

def get_bytes_for_image(image_path):
    with open(image_path, 'rb') as image_file:
        return image_file.read()

def image_path_ocr(image_path):
    appId = '11594330'
    apiKey = '6baqiIRN7EN05KrYtX5WFroM'
    secretKey = 'N65FsdDM5AsexHqdgwRyV3UIy9br8Duc'

    engine = AipOcr(appId, apiKey, secretKey)
    result = engine.general(get_bytes_for_image(image_path))
    results = []
    for wr in result['words_result']:
        results.append(wr['words'].encode("utf-8"))
    return results

if __name__ == '__main__':
    results = image_path_ocr('test2.jpg')
    for r in results:
        print(r)


def Get_Images_Tags(path):
	#return {wutil.Get_Random_Str(6)}
	print 'in get tags',image_path_ocr(path)
	return 'hello'

def Search_Image(Image):
	return 'wtf'
