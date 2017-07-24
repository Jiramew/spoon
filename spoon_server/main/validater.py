import time
from spoon_server.util.validate import validate
from spoon_server.main.manager import Manager


class Validater(Manager):
    def __init__(self, fetcher, url_prefix=None):
        super(Validater, self).__init__(url_prefix, fetcher)

    def _validate_proxy(self):
        while True:
            for each_proxy in self.database.get_all(self.generate_name(self._useful_prefix)):
                if isinstance(each_proxy, bytes):
                    each_proxy = each_proxy.decode('utf-8')
                value = self.database.getvalue(self.generate_name(self._useful_prefix), each_proxy)
                if validate(self._url_prefix, each_proxy):
                    if not value == 100:
                        self.database.inckey(self.generate_name(self._useful_prefix), each_proxy, 1)
                else:
                    if int(value) > 0:
                        self.database.set_value(self.generate_name(self._useful_prefix), each_proxy, int(int(value) / 2))
                    self.database.inckey(self.generate_name(self._useful_prefix), each_proxy, -1)
                if value and int(value) < -2:
                    self.database.delete(self.generate_name(self._useful_prefix), each_proxy)
            time.sleep(2)

    def main(self):
        self._validate_proxy()


def validater_run(url=None, fetcher=None):
    validater = Validater(url_prefix=url, fetcher=fetcher)
    validater.main()


if __name__ == '__main__':
    p = Validater("https://www.baidu.com")
    p.main()
