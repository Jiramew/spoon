from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class FPLProvider(Provider):
    def __init__(self, url_list=None, proxy=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()
        self.proxy = proxy

    @staticmethod
    def _gen_url_list():
        url_list = ["https://free-proxy-list.net/"]
        return url_list

    @Provider.provider_exception
    def getter(self):
        proxy = self.proxy  # you need to configure the proxy
        for url in self.url_list:
            tree = get_html_tree(url, proxy=proxy)
            if tree is None:
                continue
            for item in tree.xpath("//table[@id='proxylisttable']/tbody/tr"):
                ip = item.xpath("td[1]/text()")[0].strip()
                port = item.xpath("td[2]/text()")[0].strip()
                yield ip + ":" + port


if __name__ == "__main__":
    kd = FPLProvider()
    try:
        for proxy in kd.getter():
            print(proxy)
    except Exception as e:
        print(e)
