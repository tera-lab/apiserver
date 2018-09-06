# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import success_jsonify
from ..exceptions import AlreadyNoticedException, OutOfTimeException

from flask import request
from datetime import datetime
from ruamel.yaml import YAML
from google.appengine.api import memcache
import simplejson as json
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()

yaml = YAML()
webhooks = yaml.load(open('misc/gb_webhooks.yml'))

@api.route('/gquest_urgent_notify', methods=['POST'])
def gquest_urgent_notify():
  if memcache.get('gquest_urgent_notify'):
    raise AlreadyNoticedException()
  memcache.set('gquest_urgent_notify', True, 60)

  wday = datetime.now().weekday()
  bam = None
  if wday in [0, 3]:
    bam = '激昂のカラゴス'
  elif wday in [1, 4]:
    bam = '虐殺のサブラニア'
  elif wday in [2, 5]:
    bam = '貪欲のアナンシャ(vP)'

  if bam is None:
    raise OutOfTimeException()

  for webhook in webhooks:
    requests.post(
      webhook,
      json.dumps({
        'content': '@here まもなく{}が出現します'.format(bam)
      }),
      headers={'Content-Type': 'application/json'}
    )

  return success_jsonify({
    'success': 'noticed'
  })
