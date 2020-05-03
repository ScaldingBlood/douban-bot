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
        pages = ["b97827cc", "4ce63706", "5crfe930", "f3k1d581", "ce1d45977"]
        ips = []
        for page in pages:
            resp = requests.get("https://ip.ihuan.me/address/5Lit5Zu9.html?page=" + page, headers=headers)
            soup = BeautifulSoup(resp.text, "lxml")
            trs = soup.select("div.table-responsive > table > tbody > tr")
            for tr in trs:
                tds = tr.select("td")
                if tds[4].text == '支持' and tds[5].text == '支持':
                    ip = tds[0].text + ":" + tds[1].text
                    if len(ip) > 1:
                        ips.append(ip)
        for ip in ips:
            proxies = {"https": ip}
            try:
                r = requests.get(define.GROUP_URL, headers=headers, verify=False, proxies=proxies, timeout=10)
                if r.status_code == 200:
                    self.ips.append(ip)
            except:
                pass
        print(self.ips)
        self.schedler.enter(define.IP_UPDATE_INTERVAL, 0, self.update_ip)

    def select(self):
        return random.choice(self.ips)


if __name__ == "__main__":
    updater = IPUpdater()
    updater.sched_update_ip()