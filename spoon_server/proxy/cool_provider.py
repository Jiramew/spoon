import re
import base64
import codecs
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree

ip_pattern = re.compile(r'Base64.decode\(str_rot13\("([^"]+)"\)\)', re.I)


class CoolProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['https://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc/page:{0}'.format(i)
                    for i in range(1, 6)]

        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            px_segment = tree.xpath('//*[@id="main"]/table/tr')[1:]
            for px in px_segment:
                if px.xpath("./td"):
                    ip_raw = px.xpath("./td")[0].xpath("./script/text()")[0]
                    ip_find_list = ip_pattern.findall(ip_raw)
                    if ip_find_list:
                        ip_find = ip_find_list[0]
                        port = px.xpath("./td/text()")[0]
                        ip = base64.b64decode(codecs.decode(ip_find.strip(), 'rot-13')).strip().decode('utf-8')
                        yield ":".join([ip, port])


if __name__ == "__main__":
    kd = CoolProvider()
    for proxy in kd.getter():
        print(proxy)
