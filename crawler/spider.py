import requests
from verifier import util, verify
from bs4 import BeautifulSoup
from config import define


class Spider:

    def __init__(self, dbcl, ck):
        self.ck = ck
        self.dbcl = dbcl
        self.session = requests.Session()

    # def login(self, name, pwd):
    #     name = name.replace("@", "%40")
    #     url = "https://accounts.douban.com/j/mobile/login/basic?ck=&name={0:s}&password={1:s}&remember=false&ticket=".format(
    #         name, pwd)
    #
    #     headers = {
    #         'Accept-Encoding': 'gzip, deflate, br',
    #         'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    #         'Origin': 'https://accounts.douban.com',
    #         'Referer': 'https://accounts.douban.com/passport/login',
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         'Content-Length': bytes(80),
    #     }
    #     s = requests.Session()
    #
    #     resp = s.post(url, headers=headers)
    #     print(resp)
    #     jar = resp.cookies
    #     print(jar.get('bid'))
    #     print(jar.get('ck'))
    #     self.ck = jar.get('ck')
    #     print(jar.get('dbcl2'))
    #     self.dbcl = jar.get('dbcl2')

    def comment(self, url, content):
        img_url, img_id = self.get_verify_code_img(url)

        pic_path = util.save_pic_to_disk(img_url)
        verify_code = verify.get_word_in_pic(pic_path)

        comment_url = url + "add_comment"
        self.session.cookies.set_cookie(requests.cookies.create_cookie(domain='.douban.com', name='dbcl2',
                                                            value=self.dbcl))
        self.session.cookies.set_cookie(requests.cookies.create_cookie(domain='.domain.com', name='ck',
                                                            value=self.ck))
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }
        data = {"ck": self.ck, "rv_comment": content, "submit_btn": "发送", "start": 0, "captcha-solution": verify_code, "captcha-id": img_id}
        resp = self.session.post(comment_url, headers=headers, data=data)
        print(resp.text)
        print(resp)
        return url

    def get_verify_code_img(self, url):
        resp = self.session.get(url)
        soup = BeautifulSoup(resp.text, "lxml")
        img_url = soup.select(".captcha_image")[0]['src']
        pic_id = soup.select("input[name=captcha-id]")[0]['value']
        return img_url, pic_id

    @staticmethod
    def check_posts():
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }
        resp = requests.get(define.GROUP_URL, headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        items = soup.select(".olt tr")

        res = []
        for i, item in enumerate(items):
            if i > 0 and item.select(".r-count")[0].string is None:
                res.append(item.select(".title a")[0]['href'])
        return res
