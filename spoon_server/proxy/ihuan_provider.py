from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class IhuanProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['https://ip.ihuan.me/?page={}&anonymity=2'.format(str(i)) for i in range(1, 31)]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('/html/body/div[2]/div[2]/table/tbody/tr')
            for px in proxy_list:
                yield ':'.join([px.xpath('./td[1]/a/text()')[0], px.xpath('./td/text()')[0]])


if __name__ == "__main__":
    kd = IhuanProvider()
    for proxy in kd.getter():
        print(proxy)
