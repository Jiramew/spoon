import json
from spoon_server.proxy.provider import Provider
import requests


class NordProvider(Provider):
    def __init__(self, url_list=None, proxy_=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()
        self.proxy_ = proxy_

    @staticmethod
    def _gen_url_list():
        url_list = [
            "https://nordvpn.com/wp-admin/admin-ajax.php?searchParameters%5B0%5D%5Bname%5D=proxy-country&searchParameters%5B0%5D%5Bvalue%5D=&searchParameters%5B1%5D%5Bname%5D=proxy-ports&searchParameters%5B1%5D%5Bvalue%5D=&searchParameters%5B2%5D%5Bname%5D=http&searchParameters%5B2%5D%5Bvalue%5D=on&searchParameters%5B3%5D%5Bname%5D=https&searchParameters%5B3%5D%5Bvalue%5D=on&offset=0&limit=500&action=getProxies"]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            content = requests.get(url, proxies=self.proxy_).content.decode("utf-8")
            proxy_list = json.loads(content)
            for px in proxy_list:
                yield px['ip'] + ":" + px['port']


if __name__ == "__main__":
    kd = NordProvider()
    for proxy in kd.getter():
        print(proxy)
