# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import success_jsonify
from ..exceptions import OutOfTimeException, ServerUnknown, InvalidNotifyType
from ..utils import post_json

from flask import request
from datetime import datetime
from ruamel.yaml import YAML
from google.appengine.api import memcache

yaml = YAML()
webhooks = yaml.load(open('misc/gb_webhooks.yml'))


@api.route('/gquest_urgent_notify', methods=['POST'])
def gquest_urgent_notify():
    data = request.get_json()

    wday = datetime.now().weekday()
    if wday in [0, 3]:
        monster_name = '虐殺のサブラニア(崖下)'
    elif wday in [1, 4]:
        monster_name = '貪欲のアナンシャ(vP)'
    elif wday in [2, 6]:
        monster_name = '激昂のカラゴス(崖上)'
    else:
        monster_name = None

    if monster_name is None:
        raise OutOfTimeException()

    server_id = request.args.get('serverId')
    notify_type = int(request.args.get('type', -1))
    servers = {'5071': 'エリーヌ', '5073': 'ヴェリック'}
    server_name = servers.get(server_id)

    if not server_name:
        raise ServerUnknown()
    elif notify_type not in [0, 1, 3]:
        raise InvalidNotifyType()

    key = 'gquest_urgent_notify.{}.{}'.format(server_id, notify_type)
    if memcache.get(key):
        return success_jsonify({'success': 'noticed'})
    else:
        memcache.set(key, True, 60 * 30)

    if notify_type == 0:
        text = '@here まもなく{}サーバーで{}が出現します'
    elif notify_type == 1:
        text = '{}サーバーで{}が出現しました'
    elif notify_type == 3:
        text = '{}サーバーで{}が討伐されました'

    text = text.format(server_name, monster_name)
    for webhook in webhooks:
        post_json(webhook, {'content': text})

    return success_jsonify({'success': 'noticed'})
