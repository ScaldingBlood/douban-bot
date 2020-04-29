from config import define
import os
import requests
import hashlib


def save_pic_to_disk(img_url):
    if not os.path.exists(define.IMG_PATH):
        os.mkdir(define.IMG_PATH)
    resp = requests.get(img_url)
    if resp.status_code == 200:
        md5_obj = hashlib.md5()
        md5_obj.update(resp.content)
        md5_code = md5_obj.hexdigest()
        file_name = define.IMG_PATH + str(md5_code) + ".png"

        if not os.path.exists(file_name):
            with open(file_name, "wb") as f:
                f.write(resp.content)
        return file_name
    else:
        print(resp.content)
