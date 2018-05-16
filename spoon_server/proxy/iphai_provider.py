from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class IphaiProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ["http://www.iphai.com/"]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('/html/body/div[4]/div[2]/table/tr')[1:]
            for px in proxy_list:
                yield ':'.join([px.xpath('./td[1]/text()')[0].strip(), px.xpath('./td[2]/text()')[0].strip()])


if __name__ == "__main__":
    kd = IphaiProvider()
    for proxy in kd.getter():
        print(proxy)
