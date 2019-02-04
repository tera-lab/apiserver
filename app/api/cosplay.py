# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..models import Cosplay
from ..response import success_jsonify

from flask import request
from google.appengine.api import memcache


@api.route('/cosplay/list', methods=['GET'])
def cosplay_list():
    data = memcache.get('cosplayer_presets')

    if not data:
        presets = Cosplay.query().fetch()
        data = {cosplay.name: cosplay.preset for cosplay in presets}
        memcache.set('cosplayer_presets', data, 30)

    return success_jsonify(data)


@api.route('/cosplay/upload', methods=['POST'])
def cosplay_upload():
    data = request.get_json()
    for k, v in data.items():
        first = Cosplay.query(Cosplay.name == k).get()
        if first:
            first.preset = v
        else:
            first = Cosplay(name=k, preset=v)

        first.put()

    return success_jsonify({'success': 'updated'})


@api.route('/cosplay/remove', methods=['POST'])
def remove_cosplay():
    data = request.get_json()
    for name in data['characters']:
        char = Cosplay.query(Cosplay.name == name).get()
        if char:
            char.key.delete()

    return success_jsonify({'success': 'removed'})
