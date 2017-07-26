import json
import requests
from spoon_server.proxy.provider import Provider


class XunProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ["http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10"]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            content = json.loads(requests.get(url).content.decode("utf-8"))
            for row in content['RESULT']['rows']:
                yield '{}:{}'.format(row['ip'], row['port'])


if __name__ == "__main__":
    kd = XunProvider()
    for proxy in kd.getter():
        print(proxy)
