import requests
from urllib.parse import urlparse
from spoon_server.util.logger import log
from spoon_server.util.constant import HEADERS_IPHONE


def validate(target_url, proxy):
    if target_url == "default":
        target_url = "https://www.baidu.com"
        proxies = {"https": "https://{proxy}".format(proxy=proxy)}
    else:
        if urlparse(target_url).scheme == "https":
            proxies = {"https": "https://{proxy}".format(proxy=proxy)}
        else:
            proxies = {"http": "http://{proxy}".format(proxy=proxy), "https": "http://{proxy}".format(proxy=proxy)}
    try:
        r = requests.get(target_url, proxies=proxies, timeout=5, verify=False, headers=HEADERS_IPHONE)
        if r.status_code == 200:
            log.info('validate success target {0} proxy{1}'.format(target_url, proxy))
            return True
        else:
            return False
    except Exception as e:
        log.error("{0}".format(e))
        return False

if __name__ == "__main__":
    print(validate("http://www.gsxt.gov.cn/index.html", "61.160.190.34:8888"))
