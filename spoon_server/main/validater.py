import time
from multiprocessing.dummy import Pool

from spoon_server.util.validate import validate
from spoon_server.main.manager import Manager

from spoon_server.database.redis_config import RedisConfig


class Validater(Manager):
    def __init__(self, url_prefix=None, database=None, checker=None):
        super(Validater, self).__init__(database=database, url_prefix=url_prefix, checker=checker)

    def _validate_proxy(self, each_proxy):
        if isinstance(each_proxy, bytes):
            each_proxy = each_proxy.decode('utf-8')
        value = self.database.getvalue(self.generate_name(self._useful_prefix), each_proxy)
        if int(value) < 0:
            self.database.delete(self.generate_name(self._useful_prefix), each_proxy)
        else:
            if validate(self._url_prefix, each_proxy, self._checker):
                if not int(value) >= 100:
                    if int(value) == 99:
                        self.database.set_value(self.generate_name(self._hundred_prefix), each_proxy, time.time())
                    self.database.inckey(self.generate_name(self._useful_prefix), each_proxy, 1)
                else:
                    self.database.set_value(self.generate_name(self._hundred_prefix), each_proxy, time.time())
                    self.database.set_value(self.generate_name(self._useful_prefix), each_proxy, 100)
            else:
                if int(value) > 0:
                    self.database.set_value(self.generate_name(self._useful_prefix), each_proxy,
                                            int(int(value) / 2))
                self.database.inckey(self.generate_name(self._useful_prefix), each_proxy, -1)

    def main(self):
        while True:
            with Pool(10) as pool:
                proxy_list = [each_proxy for each_proxy in
                              self.database.get_all(self.generate_name(self._useful_prefix))]
                pool.map(self._validate_proxy, proxy_list)
                pool.close()
                pool.join()
                time.sleep(2)


def validater_run(url=None, database=None, checker=None):
    validater = Validater(url_prefix=url, database=database, checker=checker)
    validater.main()


if __name__ == '__main__':
    redis = RedisConfig("127.0.0.1", 21009)
    p = Validater(url_prefix="https://www.google.com", database=redis)
    p.main()
