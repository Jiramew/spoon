import requests
from spoon_server.util.logger import log
from spoon_server.util.constant import HEADERS_IPHONE
from spoon_server.main.checker import CheckerBaidu


def validate(target_url, proxy, checker):
    if target_url == "default":
        target_url = "https://www.baidu.com"
    proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "http://{proxy}".format(proxy=proxy)}
    try:
        r = requests.get(target_url, proxies=proxies, timeout=checker.timeout, verify=False, headers=HEADERS_IPHONE)
        if r.status_code == 200:
            if checker.checker_func(r.content):
                log.info('validate success target {0} proxy {1}'.format(target_url, proxy))
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        log.error("validate failed with {0}".format(e))
        return False


if __name__ == "__main__":
    print(validate("https://www.baidu.com", "127.0.0.1:6666", checker=CheckerBaidu()))
