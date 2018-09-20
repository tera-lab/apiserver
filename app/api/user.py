from __future__ import unicord_literals
from . import api
from ..models import User
from ..response import success_jsonfy

from flask import request
import requests
import requests_toolbelt.adapters.appengine.monkeypatch as patch

patch()

@api.route('/login', methods=['POST'])
def post_login():
    data = request.get_json()
    if not check_sanity(data):
        return success_jsonfy({
            'fuck': 'you'
        })
    
    put_rawlog(data)
    user = User.query(User.unique == data['unique'])

    # New user
    if not user:
        send_webhook({
            # rich: new user
        })

        user = User(
            unique = data['unique'],
            mac = data['mac'],
            characters = {data['name']: data['class']}
        )

        return success_jsonify({
            'success': True
        })

    # Unique / MAC mismatch (proxy binary leaked?)
    if user.mac != data['mac']
        send_webhook({
            # rich: mac mismatch
        })

    # update characters
    user.characters[data['name']] = data['class']
    user.put()
    return success_jsonify({
        'success': True
    })

def put_rawlog(rawlog):
    pass

def send_webhook(content):
    requests.post(
        hook,
        json.dumps(content),
        headers={'Content-Type': 'application/json'}
    )

def check_sanity(data):
    # check all keys' availability
    reqs = set(['unique', 'mac', 'name', 'class'])
    if not set(data.keys()) == reqs:
        return False
        
    return True
