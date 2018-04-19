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
        url_list = ["http://www.66ip.cn/nmtq.php?getnum=300&isp=0&"
                    "anonymoustype={0}&start=&ports=&export=&ipaddress=&area=1&proxytype=0&api=66ip".format(i) for i in
                    range(3, 5)]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            html = get_html(url, headers=HEADERS)
            if not html:
                pass
            for px in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
                yield px


if __name__ == "__main__":
    kd = SixProvider()
    for proxy in kd.getter():
        print(proxy)
