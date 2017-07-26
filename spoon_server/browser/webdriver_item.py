from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class WebDriverItem(object):
    def __init__(self, webdriver_config):
        self.webdriver_config = webdriver_config

    def get_webdriver(self):
        service_args = []

        if self.webdriver_config.proxy:
            service_args.extend([
                "--proxy=" + self.webdriver_config.proxy,
                "--proxy-type=http",
                "--ignore-ssl-errors=true"
            ])

        dcapability = dict(DesiredCapabilities.PHANTOMJS)
        if self.webdriver_config.header:
            dcapability["phantomjs.page.settings.userAgent"] = self.webdriver_config.header['User-Agent']
            dcapability["phantomjs.page.customHeaders.User-Agent"] = self.webdriver_config.header['User-Agent']
        dcapability["takesScreenshot"] = True
        driver = webdriver.PhantomJS(self.webdriver_config.phantomjs_path,
                                     service_args=service_args,
                                     desired_capabilities=dcapability)

        driver.set_page_load_timeout(self.webdriver_config.timeout)
        return driver
