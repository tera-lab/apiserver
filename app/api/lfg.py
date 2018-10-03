# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import success_jsonify

from flask import request
from datetime import datetime
from google.appengine.api import memcache


@api.route('/party_match_info', methods=['GET'])
def list_party_match_info():
    return success_jsonify(
        {
            'lfgList': memcache.get('party_match_info.lfgList') or [],
            'updated_at': memcache.get('party_match_info.updated_at')
        }
    )


@api.route('/party_match_info', methods=['POST'])
def set_party_match_info():
    data = request.get_json()
    memcache.set('party_match_info.lfgList', data['lfgList'], 60 * 30)
    memcache.set('party_match_info.updated_at', datetime.now())

    return success_jsonify({'success': 'updated'})
