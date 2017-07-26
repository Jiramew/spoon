class WebDriverPoolConfig(object):
    def __init__(self, phantomjs_path, proxy=None, header=None, timeout=10):
        self.phantomjs_path = phantomjs_path
        self.proxy = proxy
        self.header = header
        self.timeout = timeout
