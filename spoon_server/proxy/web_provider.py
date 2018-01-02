import re
import requests
from spoon_server.proxy.provider import Provider


class WebProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ["http://spys.one/pl.txt"]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            content = requests.get(url).content.decode("utf-8")
            proxy_list = re.findall("\d+\.\d+\.\d+\.\d+:\d+", content)
            for proxy in proxy_list:
                yield proxy


if __name__ == "__main__":
    kd = WebProvider()
    for proxy in kd.getter():
        print(proxy)
