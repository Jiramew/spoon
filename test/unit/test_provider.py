import unittest
from spoon_server.util.proxy_format import match_proxy_format
from spoon_server.proxy.busy_provider import BusyProvider
from spoon_server.proxy.cool_provider import CoolProvider
from spoon_server.proxy.feilong_provider import FeilongProvider
from spoon_server.proxy.gou_provider import GouProvider
from spoon_server.proxy.fpl_provider import FPLProvider
from spoon_server.proxy.gp_provider import GPProvider
from spoon_server.proxy.ihuan_provider import IhuanProvider
from spoon_server.proxy.ip31_provider import IP31Provider
from spoon_server.proxy.ip181_provider import IP181Provider
from spoon_server.proxy.ip3366_provider import IP3366Provider
from spoon_server.proxy.iphai_provider import IphaiProvider
from spoon_server.proxy.kuai_provider import KuaiProvider
from spoon_server.proxy.listende_provider import ListendeProvider
from spoon_server.proxy.mipu_provider import MimvpProvider
from spoon_server.proxy.nian_provider import NianProvider
from spoon_server.proxy.nntime_provider import NNtimeProvider
from spoon_server.proxy.nord_provider import NordProvider
from spoon_server.proxy.pdb_provider import PdbProvider
from spoon_server.proxy.plp_provider import PlpProvider
from spoon_server.proxy.prem_provider import PremProvider
from spoon_server.proxy.six_provider import SixProvider
from spoon_server.proxy.ssl_provider import SSLProvider
from spoon_server.proxy.us_provider import UsProvider
from spoon_server.proxy.wuyou_provider import WuyouProvider
from spoon_server.proxy.xiaohexia_provider import XiaohexiaProvider
from spoon_server.proxy.xici_provider import XiciProvider
from spoon_server.proxy.xun_provider import XunProvider
from spoon_server.proxy.yao_provider import YaoProvider
from spoon_server.proxy.you_provider import YouProvider
from spoon_server.proxy.zdaye_provider import ZdayeProvider


# class ProviderTestCase(unittest.TestCase):
#     def test_busy_provider(self):
#         pd = BusyProvider()
#         data = [proxy for proxy in pd.getter()]
#         self.assertTrue(len(data) > 1 and match_proxy_format(data[0]))


def add_test(name, provider):
    def test_method(provider):
        def fn(self):
            pd = provider()
            data = [proxy for proxy in pd.getter()]
            self.assertTrue(len(data) > 1 and all([match_proxy_format(p) for p in data]))

        return fn

    d = {'test': test_method(provider)}
    cls = type(name, (unittest.TestCase,), d)
    globals()[name] = cls


if __name__ == '__main__':
    for t in [BusyProvider, CoolProvider, FeilongProvider,
              FPLProvider, GouProvider, FPLProvider, GPProvider,
              IhuanProvider, IP31Provider, IP181Provider, IP3366Provider,
              IphaiProvider, KuaiProvider, ListendeProvider, MimvpProvider,
              NianProvider, NNtimeProvider, NordProvider, PdbProvider,
              PlpProvider, PremProvider, SixProvider, SSLProvider,
              UsProvider, WuyouProvider, XiaohexiaProvider, XiciProvider,
              XunProvider, YaoProvider, YouProvider, ZdayeProvider]:
        add_test(f"Test{t.__name__}", t)

    unittest.main()
