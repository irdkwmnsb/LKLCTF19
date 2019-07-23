import urllib.request, urllib.parse, base64
from . import JSONObject, API

def _login(email, pass_, app_id, scope):
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor)
    link = "https://oauth.vk.com/authorize?client_id="+str(app_id)+"&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope="+str(scope)+"&response_type=token&v=5.52"
    data = opener.open(link).read()
    lg_h = data.decode('utf-8', 'replace').split('\n      <input type="hidden" name="lg_h" value="', 1)[1].split('"', 1)[0]
    to = data.decode('utf-8', 'replace').split('\n      <input type="hidden" name="to" value="', 1)[1].split('"', 1)[0]
    data = opener.open("https://login.vk.com/?act=login&soft=1", urllib.parse.urlencode({'lg_h': lg_h, 'to': to, 'email': email, 'pass': pass_}).encode('ascii'))
    if data.geturl().startswith('https://oauth.vk.com/blank.html'):
        return data.geturl()
    data = data.read().decode('utf-8', 'replace')
    post_addr = data.split('\n    <form method="post" action="', 1)[1].split('"')[0]
    return opener.open(post_addr).geturl()

def do_login(email, pass_, app_id, scope):
    return JSONObject(dict(urllib.parse.parse_qsl(_login(email, pass_, app_id, scope).split('#', 1)[1])))

def login(email, pass_, app_id, scope):
    data = do_login(email, pass_, app_id, scope)
    return API(data.access_token, data.user_id)
