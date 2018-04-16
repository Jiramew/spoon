from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class BusyProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['https://proxy.coderbusy.com/classical/anonymous-type/highanonymous.aspx?page={0}'.format(i) for i
                    in range(1, 6)]
        url_list.extend(
            ['https://proxy.coderbusy.com/classical/anonymous-type/transparent.aspx?page={0}'.format(i) for i in
             range(1, 6)])
        url_list.extend(
            ['https://proxy.coderbusy.com/classical/anonymous-type/anonymous.aspx?page={0}'.format(i) for i in
             range(1, 6)])
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('//*[@id="site-app"]/div/div/div[1]/div/table/tbody/tr')
            for px in proxy_list:
                yield ':'.join([px.xpath('*/text()')[1].strip(), px.xpath('*/text()')[3].strip()])


if __name__ == "__main__":
    kd = BusyProvider()
    for proxy in kd.getter():
        print(proxy)
