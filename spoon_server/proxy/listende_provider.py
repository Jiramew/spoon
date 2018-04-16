import re
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree, get_html


class ListendeProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['https://www.proxy-listen.de/Proxy/Proxyliste.html']
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            response = get_html(url)
            key_pattern = re.compile('''name="fefefsfesf4tzrhtzuh" value="([^"]+)"''')
            keysearch = re.findall(key_pattern, response)
            fefefsfesf4tzrhtzuh = keysearch[0]

            post_data = {
                'filter_port': "",
                'filter_http_gateway': "",
                'filter_http_anon': "",
                'filter_response_time_http': "",
                'fefefsfesf4tzrhtzuh': fefefsfesf4tzrhtzuh,
                'filter_country': "",
                'filter_timeouts1': "",
                'liststyle': "info",
                'proxies': "200",
                'type': "httphttps",
                'submit': "Anzeigen"
            }

            tree = get_html_tree(url, data=post_data)
            if tree is None:
                continue
            px_segment = tree.xpath('//table[@class="proxyList center"]/tr')[1:]
            for px in px_segment:
                yield ":".join([px.xpath('./td/a/text()')[0], px.xpath('./td/text()')[0]])


if __name__ == "__main__":
    kd = ListendeProvider()
    for proxy in kd.getter():
        print(proxy)
