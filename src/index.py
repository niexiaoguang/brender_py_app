import os
import sys
import qiniu
import requests
import hashlib
from random import Random

def compute_md5hash(raw):
    m = hashlib.md5()
    m.update(raw.encode('utf-8'))
    return m.hexdigest()[8:-8]



def get_upload_token_pri():
    url = 'https://www.brender.cn/api/upload_token_pri'
    token = requests.get(url=url).text
    print('got upload token ' + token)
    return token;


def get_upload_token_pub():
    url = 'https://www.brender.cn/api/upload_token_pub'
    token = requests.get(url=url).text
    print('got upload token ' + token)
    return token;

img = './data/qiniu_test.jpg'
img1 = './data/qiniu_test_1.jpg'

token = get_upload_token_pub()
key = compute_md5hash(img1) + '.jpg'
ret, info = qiniu.put_file(token, key, img1)
if ret is not None:
    print(ret)
    print('All is OK')
else:
    print(info) # error message in info