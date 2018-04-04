from spoon_server.util.captcha import Captcha
from spoon_server.proxy.provider import Provider
from spoon_server.util.html_parser import get_html_tree


class MimvpProvider(Provider):
    def __init__(self, captcha_recognize_url, url_list=None):
        super(Provider, self).__init__()
        self.captcha_recognize_url = captcha_recognize_url
        if not url_list:
            self.url_list = self._gen_url_list()

    @staticmethod
    def _gen_url_list():
        url_list = ['https://proxy.mimvp.com/free.php?proxy=in_hp',
                    'https://proxy.mimvp.com/free.php?proxy=in_tp']
        return url_list

    @Provider.provider_exception
    def getter(self):
        for url in self.url_list:
            tree = get_html_tree(url)
            if tree is None:
                continue

            image_tree = tree.xpath('//*[@id="mimvp-body"]/div[2]/div/table[1]/tbody/td/img/@src')
            proxy_tree = tree.xpath('//*[@id="mimvp-body"]/div[2]/div/table[1]/tbody/td')

            image_list = ["https://proxy.mimvp.com/" + px for px in image_tree[0::2]]
            ip_list = [px.xpath('./text()')[0] for px in proxy_tree[1::10]]

            assert len(image_list) == len(ip_list)

            cap = Captcha(self.captcha_recognize_url)
            all_length = len(image_list)
            for i in range(all_length):
                try:
                    port = cap.get_image_result(image_list[i])
                    yield ip_list[i] + ":" + port
                except Exception as e:
                    yield None


if __name__ == "__main__":
    kd = MimvpProvider("Your captcha recognize url.")
    for proxy in kd.getter():
        print(proxy)
