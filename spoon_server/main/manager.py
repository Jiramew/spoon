from spoon_server.database.redis_wrapper import RedisWrapper
from spoon_server.proxy.fetcher import Fetcher
from urllib.parse import urlparse
from spoon_server.util.logger import log


class Manager(object):
    def __init__(self, url_prefix=None, fetcher=None):
        self.database = RedisWrapper("127.0.0.1", 6379)

        self._origin_prefix = 'origin_proxy'
        self._useful_prefix = 'useful_proxy'

        if not url_prefix:
            self._url_prefix = "default"
        else:
            self._url_prefix = url_prefix

        if not fetcher:
            self._fetcher = Fetcher()
        else:
            self._fetcher = fetcher

        self.log = log

    def get_netloc(self):
        if self._url_prefix == "default":
            return "default"
        return urlparse(self._url_prefix).netloc

    def generate_name(self, prefix):
        return ":".join(["spoon", self.get_netloc(), prefix])

    def refresh(self):
        if len(self._fetcher) == 0:
            raise Exception("NO PROXY PROVIDER")
        proxy_set = set()
        for provider in self._fetcher.provider_list:
            for proxy in provider.getter():
                if proxy.strip():
                    self.log.info(
                        "REFRESH FETCHER: TARGET {0} PROVIDER {1} PROXY {2}".format(self.get_netloc(),
                                                                                    provider.__class__.__name__,
                                                                                    proxy.strip()))
                    proxy_set.add(proxy.strip())
            for proxy in proxy_set:
                self.database.put(self.generate_name(self._origin_prefix), proxy)

    def get(self):
        return self.database.get(self.generate_name(self._useful_prefix))

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


if __name__ == "__main__":
    pp = Manager()
    pp.refresh()
    print(pp.get_status())
    aaa = pp.get_all_kv_from("spoon:www.gsxt.gov.cn:useful_proxy")
