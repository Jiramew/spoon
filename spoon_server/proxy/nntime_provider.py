import re
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class NNtimeProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['http://nntime.com/proxy-updated-0{0}.htm'.format(i) for i in range(1, 4)]
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue
            port_dict = {key.split("=")[0]: key.split("=")[1] for key in
                         tree.xpath("//head/script/text()")[0].strip().split(";") if key != ''}
            px_segment = tree.xpath('//*[@id="proxylist"]/tr')
            for px in px_segment:
                ip = px.xpath('./td/text()')[0]
                port = "".join([port_dict[key] for key in
                                re.findall(r"\+.*", px.xpath('./td/script/text()')[0])[0].replace(")",
                                                                                                  "").split(
                                    "+") if key != ''])
                yield ip + ":" + port


if __name__ == "__main__":
    kd = NNtimeProvider()
    for proxy in kd.getter():
        print(proxy)
