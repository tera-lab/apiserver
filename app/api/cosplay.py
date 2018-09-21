# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..models import Cosplay
from ..response import success_jsonify

from flask import request


@api.route('/cosplay/list', methods=['GET'])
def cosplay_list():
    presets = Cosplay.query().fetch()
    return success_jsonify(
        {cosplay.name: cosplay.preset
         for cosplay in presets}
    )


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
