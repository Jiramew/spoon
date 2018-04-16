import time
import requests
from lxml import etree

from spoon_server.util.constant import HEADERS
from spoon_server.util.logger import log


def get_html(url, headers=None, cookie=None, proxy=None, data=None, verify=False):
    if headers is None:
        headers = HEADERS

    try:
        if data is not None:
            response = requests.post(url=url,
                                     headers=headers,
                                     cookies=cookie,
                                     timeout=10,
                                     proxies=proxy,
                                     verify=verify,
                                     data=data)
        else:
            response = requests.get(url=url,
                                    headers=headers,
                                    cookies=cookie,
                                    timeout=10,
                                    proxies=proxy,
                                    verify=verify)
        # response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        log.error("{0}".format(e))
        raise Exception(e)


def get_html_tree(url, headers=None, cookie=None, proxy=None, data=None, verify=False):
    if headers is None:
        headers = HEADERS

    try:
        if data is not None:
            response = requests.post(url=url,
                                     headers=headers,
                                     cookies=cookie,
                                     timeout=10,
                                     proxies=proxy,
                                     verify=verify,
                                     data=data)
        else:
            response = requests.get(url=url,
                                    headers=headers,
                                    cookies=cookie,
                                    timeout=10,
                                    proxies=proxy,
                                    verify=verify)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.text
        if isinstance(html, bytes):
            html = html.decode("utf-8")
        time.sleep(1)
        return etree.HTML(html)
    except Exception as e:
        log.error("{0}".format(e))
        raise e


if __name__ == "__main__":
    tree = get_html_tree(url="http://www.baidu.com")
