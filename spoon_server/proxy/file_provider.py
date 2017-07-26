from spoon_server.proxy.provider import Provider


class FileProvider(Provider):
    @Provider.provider_exception
    def getter(self):
        yield "61.160.190.34:8888"
