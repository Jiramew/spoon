import re
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html
from spoon_server.util.constant import HEADERS


class SixProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = "http://m.66ip.cn/mo.php?sxb=&tqsl=100&port=&" \
                   "export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
        return url_list

    @Provider.provider_exception
    def getter(self):
        html = get_html(self.url_list, headers=HEADERS)
        if not html:
            pass
        for px in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield px


if __name__ == "__main__":
    kd = SixProvider()
    for proxy in kd.getter():
        print(proxy)
