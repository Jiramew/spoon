from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class ZdayeProvider(Provider):
    def __init__(self, url_list=None, proxy_=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()
        self.proxy_ = proxy_

    @staticmethod
    def _gen_url_list():
        def concatenate(port_):
            return 'http://ip.zdaye.com/?ip=&port={0}&adr=&checktime=1&sleep=3' \
                   '&cunhuo=&nport=&nadr=&dengji=&https=&yys=&post=%D6%A7%B3%D6&px='.format(port_)

        port = ['8081', '8080', '3128']
        url_list = [(p, concatenate(p)) for p in port]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for port, url in self.url_list:
            tree = get_html_tree(url, proxy=self.proxy_)
            if tree is None:
                continue
            proxy_list = tree.xpath('//*[@id="ipc"]/tbody/tr/td[1]/text()')[1:]
            for ip in proxy_list:
                yield ip + ":" + port


if __name__ == "__main__":
    kd = ZdayeProvider()
    for proxy in kd.getter():
        print(proxy)
