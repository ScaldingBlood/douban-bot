from crawler.spider import Spider
from crawler.login_util import login
from crawler.task import TaskManager
from concurrent.futures import ThreadPoolExecutor
import time
from config import define
import random

if __name__ == '__main__':

    dbcl, ck = login(define.USER_NAME, define.PASSWORD)
    spider = Spider(dbcl, ck)

    pool = ThreadPoolExecutor(8)
    comment = define.RESP_CONTENT[random.randint(0, len(define.RESP_CONTENT))]
    tm = TaskManager(spider, pool, comment)

    while True:
        urls = spider.check_posts()
        print(urls)
        tm.run(urls)
        time.sleep(define.INTERVAL)
