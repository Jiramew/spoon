import re
import execjs
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree, get_html


class KuaiProvider(Provider):
    def __init__(self, url_list=None):
        super(Provider, self).__init__()
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list(page=10):
        url_list = ['http://www.kuaidaili.com/ops/proxylist/{0}/'.format(i) for i in range(1, page + 1)]
        return url_list

    def _prepare(self):
        pre_text = get_html(self.url_list[0])
        js_string = ''.join(re.findall(r'(function .*?)</script>', pre_text))
        arg = re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', pre_text)[0]
        name = re.findall(r'function (\w+)', js_string)[0]
        js_string = js_string.replace('eval("qo=eval;qo(po);")', 'return po')
        func = execjs.compile(js_string)
        cookie_string = func.call(name, arg)
        cookie_string = cookie_string.replace("document.cookie='", "")
        clearance = cookie_string.split(';')[0]
        return {clearance.split('=')[0]: clearance.split('=')[1]}

    @Provider.provider_exception
    def getter(self):
        mode = 1
        try:
            cookie = self._prepare()
        except IndexError:
            mode = 0
        for url in self.url_list:
            if mode == 1:
                tree = get_html_tree(url, cookie=cookie)
            else:
                tree = get_html_tree(url)
            if tree is None:
                continue
            proxy_list = tree.xpath('//*[@id="freelist"]/table/tbody/tr')
            for px in proxy_list:
                yield ':'.join(px.xpath('./td/text()')[0:2])


if __name__ == "__main__":
    kd = KuaiProvider()
    for proxy in kd.getter():
        print(proxy)
