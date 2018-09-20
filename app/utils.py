# coding: utf-8
from __future__ import unicode_literals

import simplejson as json
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

def post_json(url, data):
  requests.post(
    url,
    json.dumps(data),
    headers={'Content-Type': 'application/json'}
  )
