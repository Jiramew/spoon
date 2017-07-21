import time
import schedule
from threading import Thread

from spoon_server.util.validate import validate
from spoon_server.main.manager import Manager


class Refresher(Manager):
    def __init__(self, fetcher, url_prefix=None):
        super(Refresher, self).__init__(url_prefix, fetcher)

    def _validate_proxy(self):
        origin_proxy = self.database.pop(self.generate_name(self._origin_prefix))
        exist_proxy = self.database.get_all(self.generate_name(self._origin_prefix))
        while origin_proxy:
            if validate(self._url_prefix, origin_proxy) and (origin_proxy not in exist_proxy):
                self.database.put(self.generate_name(self._useful_prefix), origin_proxy)
            origin_proxy = self.database.pop(self.generate_name(self._origin_prefix))

    def refresher_pool(self):
        self._validate_proxy()

    def main(self, process_num=20):
        self.refresh()
        proc = []
        for num in range(process_num):
            thread = Thread(target=self.refresher_pool, args=())
            proc.append(thread)

        for num in range(process_num):
            proc[num].start()

        for num in range(process_num):
            proc[num].join()


def refresher_run(url=None, fetcher=None):
    refresher = Refresher(url_prefix=url, fetcher=fetcher)
    schedule.every(5).minutes.do(refresher.main)
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    refresher_run()
