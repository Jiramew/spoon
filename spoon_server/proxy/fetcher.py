from spoon_server.proxy.gou_provider import GouProvider
from spoon_server.proxy.kuai_provider import KuaiProvider
from spoon_server.proxy.xici_provider import XiciProvider
from spoon_server.proxy.kuai_pay_provider import KuaiPayProvider
from spoon_server.proxy.file_provider import FileProvider
from spoon_server.proxy.wuyou_provider import WuyouProvider
from spoon_server.proxy.us_provider import UsProvider


class Fetcher(object):
    def __init__(self, use_default=True):
        if use_default:
            self.provider_list = self._generate_provider_list()
        else:
            self.provider_list = []

    @staticmethod
    def _generate_provider_list():
        gp = GouProvider()
        kp = KuaiProvider()
        kpp = KuaiPayProvider()
        xp = XiciProvider()
        fp = FileProvider()
        wp = WuyouProvider()
        up = UsProvider()
        return [up, gp, kp, kpp, xp, fp, wp]

    def clear(self):
        self.provider_list = []
        return self

    def set_provider(self, providers):
        self.provider_list = providers
        return self

    def __len__(self):
        return len(self.provider_list)


if __name__ == '__main__':
    fetch = Fetcher()

    for k in fetch.provider_list:
        for px in k.getter():
            print(px)
