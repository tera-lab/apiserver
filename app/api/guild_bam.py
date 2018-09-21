# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import success_jsonify
from ..exceptions import OutOfTimeException
from ..utils import post_json

from flask import request
from datetime import datetime
from ruamel.yaml import YAML
from google.appengine.api import memcache

yaml = YAML()
webhooks = yaml.load(open('misc/gb_webhooks.yml'))

@api.route('/gquest_urgent_notify', methods=['POST'])
def gquest_urgent_notify():
  if memcache.get('gquest_urgent_notify'):
    return success_jsonify({
      'success': 'noticed'
    })

  wday = datetime.now().weekday()
  bam = None
  if wday in [0, 3]:
    bam = '虐殺のサブラニア(崖下)'
  elif wday in [1, 4]:
    bam = '貪欲のアナンシャ(vP)'
  elif wday in [2, 6]:
    bam = '激昂のカラゴス(崖上)'

  if bam is None:
    raise OutOfTimeException()

  memcache.set('gquest_urgent_notify', True, 60)
  for webhook in webhooks:
    post_json(webhook, {
      'content': '@here まもなく{}が出現します'.format(bam)
    })

  return success_jsonify({
    'success': 'noticed'
  })
