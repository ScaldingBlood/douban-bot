import requests
from bs4 import BeautifulSoup
import time
import sched
import random
from config import define
import threading


class IPUpdater:
    def __init__(self):
        self.ips = []
        self.schedler = sched.scheduler(time.time, time.sleep)

    def sched_update_ip(self):
        self.update_ip()
        self.schedler.enter(define.IP_UPDATE_INTERVAL, 0, self.update_ip)
        t = threading.Thread(target=self.schedler.run)
        t.setDaemon(True)
        t.start()

    def update_ip(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        }
        resp = requests.get("https://ip.ihuan.me/address/5Lit5Zu9.html", headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        trs = soup.select("div.table-responsive > table > tbody > tr")
        ips = []
        for tr in trs:
            tds = tr.select("td")
            ip = tds[0].text + ":" + tds[1].text
            if len(ip) > 1:
                print(ip)
                ips.append(ip)
        self.ips = ips
        self.schedler.enter(define.IP_UPDATE_INTERVAL, 0, self.update_ip)

    def select(self):
        return random.choice(self.ips)


if __name__ == "__main__":
    updater = IPUpdater()
    updater.sched_update_ip()