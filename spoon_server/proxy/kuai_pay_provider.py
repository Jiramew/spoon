from spoon_server.proxy.provider import Provider
import requests


class KuaiPayProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = []
        return url_list

    def getter(self):
        for url in self.url_list:
            content = requests.get(url).content.decode("utf-8")
            proxy_list = content.split("\r\n")
            for px in proxy_list:
                yield px.strip()


if __name__ == "__main__":
    kd = KuaiPayProvider()
    for proxy in kd.getter():
        print(proxy)
