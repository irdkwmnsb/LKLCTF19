import requests


class FishText():
    URL = "https://fish-text.ru/get"

    def __init__(self):
        self.session = requests.Session()

    def request(self, type, n):
        r = self.session.get(self.URL, params={"type": type, "number": n, "format": "json"})
        a = r.json()
        if a['status'] == 'success':
            return a['text'].replace("\\n", "\n")
        else:
            raise Exception(a)

    def sentence(self, n=3):
        return self.request("sentence", n)

    def paragraph(self, n=3):
        return self.request("paragraph", n)

    def title(self, n=1):
        return self.request("title", n)

