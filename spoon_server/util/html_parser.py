import time
import requests
from lxml import etree

from spoon_server.util.constant import HEADERS
from spoon_server.util.logger import log


def get_html(url, headers=None):
    if headers is None:
        headers = HEADERS

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        log.error("{0}".format(e))
        return


def get_html_tree(url, headers=None):
    if headers is None:
        headers = HEADERS

    try:
        response = requests.get(url=url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        html = response.content
        if isinstance(html, bytes):
            html = html.decode("utf-8")
        time.sleep(1)
        return etree.HTML(html)
    except Exception as e:
        log.error("{0}".format(e))
        return


if __name__ == "__main__":
    tree = get_html_tree(url="http://www.baidu.com")
