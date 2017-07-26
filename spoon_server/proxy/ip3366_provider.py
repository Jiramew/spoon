from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class IP3366Provider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        base_url_list = ['http://www.ip3366.net/free/?stype={0}&page='.format(i) for i in range(1, 5)]
        url_list = [url + str(j) for url in base_url_list for j in range(1, 5)]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('//*[@id="list"]/table//tr')
            for px in proxy_list[1:]:
                yield ':'.join(px.xpath('./td/text()')[0:2])


if __name__ == "__main__":
    kd = IP3366Provider()
    for proxy in kd.getter():
        print(proxy)
