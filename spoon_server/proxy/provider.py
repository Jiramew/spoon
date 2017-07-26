class Provider(object):
    def __init__(self):
        self.url_list = None
        pass

    def getter(self):
        pass

    @classmethod
    def provider_exception(cls, fun):
        def wrapper(self, *args, **kwargs):
            try:
                return fun(self, *args, **kwargs)
            except Exception as e:
                raise e

        return wrapper

    # def __str__(self):
    #     return self.__class__.__name__
