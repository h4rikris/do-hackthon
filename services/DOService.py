import json

import requests


class DOService:

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get(self, url, params=None):
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer %s' % self.token}
        response = requests.get("%s%s" % (self.url, url), headers=headers, params=params)
        return response.json()
