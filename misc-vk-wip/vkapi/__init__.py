import requests, json

class API(object):
    API_VERSION = '5.78'
    def __init__(self, token, uid=None):
        self.token = token
        self.self = uid
    def call(self, method, **kwargs):
        if 'v' not in kwargs:
            kwargs['v'] = self.API_VERSION
        kwargs['access_token'] = kwargs.get('access_token', self.token)
        data = requests.post('https://api.vk.com/method/'+method, kwargs)
        data = json.loads(data.text, object_hook=JSONObject)
        return data
    def execute(self, code):
        return self.call('execute', code=code)
    def __getattr__(self, nname):
        self.__dict__[nname] = Namespace(self, nname)
        return self.__dict__[nname]

class Namespace(object):
    def __init__(self, api, nsname):
        self.api = api
        self.name = nsname
    def __getattr__(self, fname):
        full_name = self.name + '.' + fname
        def func(**kwargs):
            return self.api.call(full_name, **kwargs)
        func.__name__ = func.__qualname__ = full_name
        self.__dict__[fname] = func
        return func

class JSONObject(dict):
    def __getattr__(self, attr):
        try: return self[attr]
        except KeyError:
            if attr.startswith('vk_') and attr[3:] in self:
                return self[attr[3:]]
            raise AttributeError(self)
