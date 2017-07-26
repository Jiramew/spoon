import re
import json
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html


class GPProvider(Provider):
    def __init__(self, url_list=None, proxy=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()
        self.proxy = proxy

    @staticmethod
    def _gen_url_list():
        cy_list = ["China", "Indonesia", "United%20States", "Brazil", "Russia", "Thailand", "India", "United%20Kingdom",
                   "Bangladesh", "Germany", "Singapore"]
        base_url_list = ["http://www.gatherproxy.com/proxylist/country/?c=" + cy for cy in cy_list]

        url_list = [url for url in base_url_list]
        return url_list

    @Provider.provider_exception
    def getter(self):
        proxy = self.proxy  # you need to configure the proxy
        for url in self.url_list:
            tree = get_html(url, proxy=proxy)
            if tree is None:
                continue
            pattern = re.compile('gp.insertPrx\((.*?)\)', re.RegexFlag.S)
            items = re.findall(pattern, tree)
            for item in items:
                data = json.loads(item)
                port = data.get('PROXY_PORT')
                port = str(int(port, 16))

                yield data.get('PROXY_IP') + ":" + port


if __name__ == "__main__":
    kd = GPProvider()
    try:
        for proxy in kd.getter():
            print(proxy)
    except Exception as e:
        print(e)
