import re


def match_proxy_format(origin):
    return re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', origin) is not None
