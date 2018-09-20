# coding: utf-8
from __future__ import unicode_literals

import simplejson as json
import requests
from requests_toolbelt.adapters.appengine import monkeypatch as patch

patch()


def post_json(url, data):
    requests.post(
        url,
        json.dumps(data),
        headers={'Content-Type': 'application/json'}
    )

class DictWrapper():
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            return None

    def __setattr__(self, name, value):
        self._data[name] = value
