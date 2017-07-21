import time
from multiprocessing import Process

from spoon_server.main.proxy_pipe import ProxyPipe


def main_run():
    p1 = ProxyPipe(url_prefix="https://www.baidu.com")
    p2 = ProxyPipe(url_prefix="https://www.google.com")
    p3 = ProxyPipe()

    proc_list = [Process(target=p1.start), Process(target=p2.start), Process(target=p3.start)]

    for p in proc_list:
        p.start()
        time.sleep(1)
    for p in proc_list:
        p.join()

if __name__ == '__main__':
    main_run()
