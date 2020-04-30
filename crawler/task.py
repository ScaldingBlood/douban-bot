from crawler.spider import Spider
import threading


class TaskManager:
    # _local = threading.local()

    def __init__(self, post_utils, pool):
        # TaskManager._local.urls = dict()
        self.post_utils = post_utils
        self.pool = pool
        self.processing = {}

    def run(self, urls):
        processing = {}
        for url in urls:
            processing[url] = True
            # if url not in TaskManager._local.urls.keys():
            if url not in self.processing:
                # TaskManager._local.urls[url] = True
                self.pool.submit(Spider.comment, self.post_utils, url)
                # .add_done_callback(TaskManager.clean_callback)
        self.processing = processing

    @staticmethod
    def clean_callback(r):
        res = r.result()
        # del TaskManager._local.urls[res]
