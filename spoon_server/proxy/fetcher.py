import copy
from spoon_server.proxy.gou_provider import GouProvider
from spoon_server.proxy.kuai_provider import KuaiProvider
from spoon_server.proxy.xici_provider import XiciProvider
from spoon_server.proxy.wuyou_provider import WuyouProvider
from spoon_server.proxy.us_provider import UsProvider
from spoon_server.proxy.ip181_provider import IP181Provider
from spoon_server.proxy.six_provider import SixProvider


class Fetcher(object):
    def __init__(self, use_default=True):
        if use_default:
            self.provider_list = self._generate_provider_list()
        else:
            self.provider_list = []
        self.origin_provider_list = []

    @staticmethod
    def _generate_provider_list():
        ip181 = IP181Provider()
        gp = GouProvider()  # Maybe IP Block
        kp = KuaiProvider()  # Maybe malfunction
        # kpp = KuaiPayProvider()
        xp = XiciProvider()
        # fp = FileProvider()
        wp = WuyouProvider()  # Maybe IP Block
        up = UsProvider()
        six = SixProvider()
        return [ip181, up, gp, kp, xp, wp, six]

    def clear(self):
        self.provider_list = []
        return self

    def set_provider(self, providers):
        self.provider_list = providers
        return self

    def add_provider(self, providers):
        self.provider_list.extend(providers)
        return self

    def get_provider(self, index):
        return self.provider_list[index]

    def remove_provider(self, indices):
        indices.reverse()
        for index in indices:
            self.provider_list.pop(index)

    def backup_provider(self):
        self.origin_provider_list = copy.deepcopy(self.provider_list)

    def restore_provider(self):
        self.provider_list = self.origin_provider_list[:]

    def __len__(self):
        return len(self.provider_list)

    def __str__(self):
        return "|".join(p.__class__.__name__ for p in self.provider_list)


if __name__ == '__main__':
    fetch = Fetcher()

    for k in fetch.provider_list:
        for px in k.getter():
            print(px)
