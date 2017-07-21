from spoon_server.proxy.fetcher import Fetcher
from spoon_server.main.proxy_pipe import ProxyPipe
from spoon_server.proxy.us_provider import UsProvider


def main_run():
    p1 = ProxyPipe(url_prefix="https://www.google.com", fetcher=Fetcher(use_default=False)).set_fetcher([UsProvider()])
    p1.start()

if __name__ == '__main__':
    main_run()
