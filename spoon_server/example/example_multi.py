import time
from multiprocessing import Process

from spoon_server.main.proxy_pipe import ProxyPipe
from spoon_server.database.redis_config import RedisConfig
from spoon_server.main.checker import CheckerBaidu


def main_run():
    redis = RedisConfig("127.0.0.1", 21009)
    p1 = ProxyPipe(url_prefix="https://www.baidu.com", database=redis, checker=CheckerBaidu())
    p2 = ProxyPipe(url_prefix="https://www.google.com", database=redis)
    p3 = ProxyPipe(database=redis)

    proc_list = [Process(target=p1.start), Process(target=p2.start), Process(target=p3.start)]

    for p in proc_list:
        p.start()
        time.sleep(1)
    for p in proc_list:
        p.join()


if __name__ == '__main__':
    main_run()
