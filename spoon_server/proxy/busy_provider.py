from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class BusyProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['https://proxy.coderbusy.com/zh-cn/classical/anonymous-type/highanonymous/p{0}.aspx'.format(i) for i
                    in range(1, 5)]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('/html/body/main/div[2]/div/div/div[1]/div/div/table//tr')
            for px in proxy_list[1:]:
                yield ':'.join([px.xpath('./td/text()')[1].strip(), px.xpath('./td/text()')[2].strip()])


if __name__ == "__main__":
    kd = BusyProvider()
    for proxy in kd.getter():
        print(proxy)
