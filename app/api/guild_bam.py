# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import success_jsonify
from ..exceptions import OutOfTimeException, ServerUnknown
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
    servers = {'5071': 'エリーヌ', '5073': 'ヴェリック'}
    server_name = servers.get(server_id)
    if not server_name:
        raise ServerUnknown()

    key = 'gquest_urgent_notify.{}'.format(server_id)
    if memcache.get(key):
        return success_jsonify({'success': 'noticed'})
    else:
        memcache.set(key, True, 60 * 30)

    for webhook in webhooks:
        post_json(
            webhook, {
                'content':
                    '@here まもなく{}サーバーで{}が出現します'.
                    format(server_name, monster_name)
            }
        )

    return success_jsonify({'success': 'noticed'})
