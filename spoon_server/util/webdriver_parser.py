from lxml import etree
from spoon_server.util.logger import log
from spoon_server.util.constant import HEADERS

from spoon_server.browser.webdriver_pool import WebdriverPool
from spoon_server.browser.webdriver_pool_config import WebDriverPoolConfig


class WebdriverParser(object):
    def __init__(self, header=None, proxy=None):
        if header is None:
            header = HEADERS
        self.wdp_config = WebDriverPoolConfig(
            phantomjs_path="D:/program/phantomjs-2.1.1-windows/bin/phantomjs.exe",
            header=header,
            proxy=proxy
        )
        self.wd = WebdriverPool(self.wdp_config)
        self.driver = self.wd.acquire()

    def parse(self, url):
        try:
            self.driver.get(url)
            html = self.driver.page_source

            return etree.HTML(html)
        except Exception as e:
            log.error("{0}".format(e))
            raise Exception(e)
        finally:
            self.wd.release(self.driver)
            self.wd.stop()
