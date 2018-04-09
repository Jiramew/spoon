from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class GouProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ["http://www.goubanjia.com"]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            table = tree.xpath('//table/tbody/tr')
            for tb in table:
                component = tb.xpath('td[@class="ip"]/*[not(@style="display: none;" or @style="display:none;")]/text()')
                component.insert(-1, ':')
                yield "".join(component)


if __name__ == "__main__":
    kd = GouProvider()
    try:
        for proxy in kd.getter():
            print(proxy)
    except Exception as e:
        print(e)
