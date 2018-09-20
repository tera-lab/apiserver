# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..models import Character, User, Logger
from ..response import success_jsonify
from ..utils import post_json

from flask import request
from google.appengine.ext import ndb


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query(User.unique == data['unique']).get()
    character = Character.query(ndb.AND(
        Character.serverId == data['serverId'],
        Character.playerId == data['playerId']
    )).get()

    if user:
        if data['mac'] == 'Unknown':
            pass
        # Unique / MAC mismatch
        elif user.mac != data['mac']:
            post_json('https://discordapp.com/api/webhooks/492357190259310603/mS7liQAUsqVUw_Y_7Hsq5klrGfFhv5tvSNOiRLBqeuNyHfajyX8H_5yYk62FuhHrUnmn', {
                'username': 'warning',
                'embeds': [{
                    'description': '<@&479964532949778432> unique[{}]のMACアドレスが登録アドレスと異なっています'.format(user.unique),
                    'color': 0xff4757,
                    'fields': [
                        {
                            'name': 'Registered MAC',
                            'value': user.mac,
                            'inline': True
                        }, {
                            'name': 'Posted Mac',
                            'value': data['mac'],
                            'inline': True
                        }
                    ]
                }]
            })
            user = User(unique=data['unique'], mac=data['mac'])
    else:
        user = User(unique=data['unique'], mac=data['mac'])

    # new character
    if not character:
        character = Character(
            serverId=data['serverId'],
            playerId=data['playerId'],
            name=data['name'],
            job=data['job']
        )
        character.put()

    if not filter(lambda key: character.key == key, user.characters):
        user.characters.append(character.key)

    user.put()
    # Logger.insert(stuff)
    return success_jsonify({
        'success': True
    })
