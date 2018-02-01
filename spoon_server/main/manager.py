import time
from urllib.parse import urlparse

from spoon_server.database.redis_wrapper import RedisWrapper
from spoon_server.proxy.fetcher import Fetcher
from spoon_server.main.checker import Checker
from spoon_server.util.logger import log


class Manager(object):
    def __init__(self, database=None, url_prefix=None, fetcher=None, checker=None):
        if not database:
            self.database = RedisWrapper("127.0.0.1", 6379, 0)
        else:
            self.database = RedisWrapper(database.host, database.port, database.db, database.password)

        self._origin_prefix = 'origin_proxy'
        self._useful_prefix = 'useful_proxy'
        self._hundred_prefix = 'hundred_proxy'
        self._current_prefix = 'current_proxy'

        if not url_prefix:
            self._url_prefix = "default"
        else:
            self._url_prefix = url_prefix

        if not fetcher:  # validater
            self._fetcher = Fetcher()
        else:  # refresher
            self._fetcher = fetcher
            self._fetcher.backup_provider()
            log.error("REFRESH FETCHER BACKUP PROVIDER {0}".format(str(self._fetcher)))

        if not checker:
            self._checker = Checker()
        else:
            self._checker = checker

        self.log = log

    def get_netloc(self):
        if self._url_prefix == "default":
            return "default"
        return urlparse(self._url_prefix).netloc

    def generate_name(self, prefix):
        return ":".join(["spoon", self.get_netloc(), prefix])

    def refresh_condition(self):
        all_proxy_score = [[k.decode('utf-8'), int(v.decode('utf-8'))] for (k, v) in
                           self.get_all_kv_from(self.generate_name(self._useful_prefix)).items()]

        all_length = len(all_proxy_score)
        count_length = len([0 for (k, v) in all_proxy_score if v >= 95])

        if all_length <= 100:
            return True

        if count_length / all_length >= 0.2:
            return True
        else:
            return False

    def refresh(self):
        log.info("REFRESH START WITH {0} TARGET {1}".format(str(self._fetcher), self.get_netloc()))
        if not self.refresh_condition():
            log.info("REFRESH DID NOT MEET CONDITION. TARGET{0}".format(self.get_netloc()))
            return

        if len(self._fetcher) < 3:
            self._fetcher.restore_provider()
            log.info("REFRESH FETCHER FAILED: NO ENOUGH PROVIDER, RESTORE PROVIDERS TO {0}. TARGET {1}".format(
                str(self._fetcher), self.get_netloc()))
        proxy_set = set()

        provider_to_be_removed_index = []
        for index in range(len(self._fetcher)):
            provider = self._fetcher.get_provider(index)
            try:
                for proxy in provider.getter():
                    if proxy.strip():
                        self.log.info(
                            "REFRESH FETCHER: TARGET {0} PROVIDER {1} PROXY {2}".format(self.get_netloc(),
                                                                                        provider.__class__.__name__,
                                                                                        proxy.strip()))
                        proxy_set.add(proxy.strip())
            except Exception as e:
                provider_to_be_removed_index.append(index)
                log.error(
                    "REFRESH FETCHER FAILED: PROVIDER {0} WILL BE REMOVED ERROR {1}".format(provider.__class__.__name__,
                                                                                            e))

            for proxy in proxy_set:
                self.database.set_value("spoon:proxy_stale", proxy, time.time())
                self.database.put(self.generate_name(self._origin_prefix), proxy)

        log.info("REFRESH FETCHER DELETE {0}. TARGET {1}".format(provider_to_be_removed_index, self.get_netloc()))
        self._fetcher.remove_provider(provider_to_be_removed_index)

    def get(self):
        return self.database.get(self.generate_name(self._useful_prefix))

    def set_value(self, key, value):
        return self.database.set_value(self.generate_name(self._useful_prefix), key, value)

    def delete(self, proxy):
        self.database.delete(self.generate_name(self._useful_prefix), proxy)

    def get_all(self):
        return self.database.get_all(self.generate_name(self._useful_prefix))

    def get_status(self):
        total_origin_proxy = self.database.get_status(self.generate_name(self._origin_prefix))
        total_useful_queue = self.database.get_status(self.generate_name(self._useful_prefix))
        return {'origin_proxy': total_origin_proxy, 'useful_proxy': total_useful_queue}

    # For spoon_web
    def get_keys(self):
        return [key.decode("utf-8") for key in self.database.get_keys()]

    def get_from(self, target):
        return self.database.get(target)

    def get_all_from(self, target):
        return self.database.get_all(target)

    def get_all_kv_from(self, target):
        return self.database.get_all_kv(target)

    def get_range_from(self, target):
        return self.database.zrange(target, 0, -1)


if __name__ == "__main__":
    pp = Manager()
    pp.refresh()
    print(pp.get_status())
    aaa = pp.get_all_kv_from("spoon:www.gsxt.gov.cn:useful_proxy")
