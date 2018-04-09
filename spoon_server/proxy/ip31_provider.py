import re
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html
from spoon_server.util.constant import HEADERS


class IP31Provider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = "https://31f.cn/http-proxy/"
        return url_list

    @Provider.provider_exception
    def getter(self):
        html = get_html(self.url_list, headers=HEADERS)
        if not html:
            pass
        for px in re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>\n<td>(\d{1,5})</td>', html, re.S):
            yield ":".join(px)


if __name__ == "__main__":
    kd = IP31Provider()
    for proxy in kd.getter():
        print(proxy)
