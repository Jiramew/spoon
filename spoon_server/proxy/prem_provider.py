from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree

port_dict = {
    're4e8': '8080', 'r1819': '80', 'ra572': '53281',
    'r0a84': '3128', 'r0f89': '8888', 'raa30': '8088',
    'r93ce': '81', 'rf015': '65309', 'rc8e9': '544',
    'r479e': '20183', 'r6666': '8081', 'r70fb': '55555',
    're048': '8118', 'rac4c': '9000', 'r6446': '18118',
    'r23aa': '8060', 'r626c': '61234', 'r1adf': '62225',
    're04a': '54314', 'r4928': '3129', 'ra1ab': '3100',
    'rc6b5': '8383', 'rd026': '8380', 'r007c': '808',
    'r3d4e': '8000', 'rd376': '61588', 'refa9': '45618',
    'r1986': '31588', 'r39d8': '65301', 'r5665': '3355',
    'rb2b3': '53282', 'r562f': '53005', 'r6f48': '52136',
    'ra5c1': '443', 're42f': '65205', 'r0450': '54214',
    'r0b20': '3130', 'r74c4': '65103', 'r7d8f': '37777',
    'r96fd': '7777', 'r0df1': '87', 'r2da5': '52225'
}


class PremProvider(Provider):
    def __init__(self, url_list=None, proxy=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()
        self.proxy = proxy

    @staticmethod
    def _gen_url_list():
        url_list = ['https://premproxy.com/list/0{0}.htm'.format(i)
                    for i in range(1, 3)]

        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url, proxy=self.proxy)
            if tree is None:
                continue
            px_segment = tree.xpath('//*[@id="proxylistt"]/tbody/tr')[:-1]
            for px in px_segment:
                ip = px.xpath('./td')[0].xpath('./span')[0].tail
                port = port_dict[px.xpath('./td')[0].xpath('./span')[1].xpath("@class")[0]]
                yield ip + port


if __name__ == "__main__":
    kd = PremProvider()
    for proxy in kd.getter():
        print(proxy)
