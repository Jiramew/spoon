import concurrent.futures
from spoon_server.proxy.busy_provider import BusyProvider
from spoon_server.proxy.cool_provider import CoolProvider
from spoon_server.proxy.feilong_provider import FeilongProvider
from spoon_server.proxy.fpl_provider import FPLProvider
from spoon_server.proxy.gou_provider import GouProvider
from spoon_server.proxy.gp_provider import GPProvider
from spoon_server.proxy.ihuan_provider import IhuanProvider
from spoon_server.proxy.ip31_provider import IP31Provider
from spoon_server.proxy.ip181_provider import IP181Provider
from spoon_server.proxy.ip3366_provider import IP3366Provider
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
from spoon_server.proxy.web_provider import WebProvider
from spoon_server.proxy.wuyou_provider import WuyouProvider
from spoon_server.proxy.xiaohexia_provider import XiaohexiaProvider
from spoon_server.proxy.xici_provider import XiciProvider
from spoon_server.proxy.xun_provider import XunProvider
from spoon_server.proxy.yao_provider import YaoProvider
from spoon_server.proxy.you_provider import YouProvider
from spoon_server.proxy.zdaye_provider import ZdayeProvider

all_provider_list = [
    BusyProvider, CoolProvider, FeilongProvider, FPLProvider, GouProvider, GPProvider,
    IhuanProvider, IP31Provider, IP181Provider, IP3366Provider, KuaiProvider, ListendeProvider,
    MimvpProvider, NianProvider, NNtimeProvider, NordProvider, PdbProvider, PlpProvider,
    PremProvider, SixProvider, SSLProvider, UsProvider, WebProvider, WuyouProvider,
    XiaohexiaProvider, XiciProvider, XunProvider, YaoProvider, YouProvider, ZdayeProvider
]


def check_provider(pro):
    current_proxies = []
    try:
        pro_instance = pro()
    except Exception as e:
        print(pro.__name__, e)
        return

    try:
        for p in pro_instance.getter():
            current_proxies.append(p)
        print(pro_instance.__class__.__name__, len(current_proxies))
    except Exception as e:
        print(pro_instance.__class__.__name__, len(current_proxies), e)


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        for pro in all_provider_list:
            executor.submit(check_provider, pro)
