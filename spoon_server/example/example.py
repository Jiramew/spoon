from spoon_server.proxy.fetcher import Fetcher
from spoon_server.main.proxy_pipe import ProxyPipe
from spoon_server.proxy.kuai_provider import KuaiProvider
from spoon_server.proxy.xici_provider import XiciProvider
from spoon_server.database.redis_config import RedisConfig
from spoon_server.main.checker import CheckerBaidu


def main_run():
    redis = RedisConfig("127.0.0.1", 21009)
    p1 = ProxyPipe(url_prefix="https://www.baidu.com",
                   fetcher=Fetcher(use_default=False),
                   database=redis,
                   checker=CheckerBaidu()).set_fetcher([KuaiProvider()]).add_fetcher([XiciProvider()])
    p1.start()


if __name__ == '__main__':
    main_run()
