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
        pages = [1]
        ips = []
        for page in pages:
            resp = requests.get("https://www.xicidaili.com/wn/" + str(page), headers=headers)
            soup = BeautifulSoup(resp.text, "lxml")
            trs = soup.select(".odd")
            for tr in trs:
                tds = tr.select("td")
                ip = tds[1].text + ":" + tds[2].text
                if len(ip) > 1:
                    ips.append(ip)
        for ip in ips:
            proxies = {"https": ip}
            try:
                r = requests.get(define.GROUP_URL, headers=headers, verify=False, proxies=proxies, timeout=10)
                if r.status_code == 200:
                    self.ips.append(ip)
                    if len(self.ips) > 9:
                        break
            except:
                pass
        print(self.ips)
        self.schedler.enter(define.IP_UPDATE_INTERVAL, 0, self.update_ip)

    def select(self):
        if len(self.ips) == 0:
            return None
        return random.choice(self.ips)


if __name__ == "__main__":
    updater = IPUpdater()
    updater.sched_update_ip()