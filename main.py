from crawler.spider import Spider
from crawler.login_util import login
from crawler.task import TaskManager
from crawler.ip_util import IPUpdater
from concurrent.futures import ThreadPoolExecutor
import time
from config import define

if __name__ == '__main__':
    ipUpdater = IPUpdater()
    ipUpdater.sched_update_ip()

    dbcl, ck, bid = login(define.USER_NAME, define.PASSWORD)
    # dbcl, ck = None, None
    spider = Spider(dbcl, ck, bid)

    pool = ThreadPoolExecutor(8)
    tm = TaskManager(spider, pool)

    while True:
        urls = spider.check_posts(ipUpdater.select())
        print(urls)
        tm.run(urls)
        time.sleep(define.INTERVAL)
