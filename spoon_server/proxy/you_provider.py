import re
import requests
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree
from spoon_server.util.constant import HEADERS


class YouProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        try:
            url_list = get_html_tree("http://www.youdaili.net/Daili/http/").xpath(
                './/div[@class="chunlist"]/ul/li/p/a/@href')[0:1]
            return url_list
        except Exception as e:
            raise e

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            html = requests.get(url, headers=HEADERS).content
            if not html:
                continue
            proxy_list = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html)
            for px in proxy_list:
                yield px


if __name__ == "__main__":
    try:
        kd = YouProvider()
        aaa = kd.getter()
        for proxy in aaa:
            print(proxy)
    except Exception as e:
        print(str(e))
