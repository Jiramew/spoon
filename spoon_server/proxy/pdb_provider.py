import re
import execjs
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class PdbProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['http://proxydb.net/?protocol=http&protocol=https',
                    ]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('/html/body/div[2]/table//tr')
            for px in proxy_list[1:]:
                script_string = 'function func() {var proxies=[];' + (
                    re.sub("document.*?;", "",
                           ''.join(px.xpath('./td[1]/script/text()'))) + "; return proxies}").replace(
                    "\n", "")
                js_string = execjs.compile(script_string)
                result = js_string.call('func')
                yield result[0]


if __name__ == "__main__":
    kd = PdbProvider()
    for proxy in kd.getter():
        print(proxy)
