from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class GouProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list(page=2):
        base_url_list = ["http://www.goubanjia.com/free/gngn/index{0}.shtml",
                         "http://www.goubanjia.com/free/gwgn/index{0}.shtml",
                         "http://www.goubanjia.com/free/gwpt/index{0}.shtml"]

        url_list = [url.format(j) for url in base_url_list for j in range(1, page)]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            px_segment = tree.xpath("//table[@ class='table']/tbody/tr")
            for px in px_segment:
                yield "".join(px.xpath(
                    "./td[@class='ip']/span/text() | ./td[@class='ip']/div/text()|./td[@class='ip']/text()"))


if __name__ == "__main__":
    kd = GouProvider()
    try:
        for proxy in kd.getter():
            print(proxy)
    except Exception as e:
        print(e)
