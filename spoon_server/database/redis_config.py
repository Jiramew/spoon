class RedisConfig(object):
    def __init__(self, host, port, db=0, password=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
