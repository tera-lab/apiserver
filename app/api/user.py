# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..models import Character, User, Logger
from ..response import success_jsonify
from ..utils import post_json, DictWrapper

from flask import request
from google.appengine.ext import ndb


WEBHOOK = 'https://discordapp.com/api/webhooks/492357190259310603/mS7liQAUsqVUw_Y_7Hsq5klrGfFhv5tvSNOiRLBqeuNyHfajyX8H_5yYk62FuhHrUnmn'

@api.route('/login', methods=['POST'])
def login():
    data = DictWrapper(request.get_json())
    user = User.query(User.unique == data.unique).get()
    character = Character.query(ndb.AND(
        Character.serverId == data.serverId,
        Character.playerId == data.playerId
    )).get()

    # User exists
    if user:
        # update MAC if failed to get before
        if user.mac == 'Unknown' and data.mac != 'Unknown':
            user.mac = data.mac
        # Unique / MAC mismatch
        elif user.mac != data.mac:
            post_json(
                WEBHOOK,
                {
                    'username': 'Warning',
                    'embeds': [{
                        'description': 'Unique / MAC mismatch!',
                        'color': 0xff4757,
                        'fields': [
                            {
                                'name': 'Unique',
                                'value': user.unique
                            },
                            {
                                'name': 'Expected MAC',
                                'value': user.mac,
                                'inline': True
                            },
                            {
                                'name': 'Detected MAC',
                                'value': data.mac,
                                'inline': True
                            }
                        ]
                    }]
                }
            )

    # New user, **MUST BE ALERTED!**
    else:
        post_json(
            WEBHOOK,
            'username': 'Information',
            'embeds': [{
                'description': 'New User',
                'color': 0x42f4ee,
                'fields': [
                    {
                        'name': 'Unique',
                        'value': data.unique,
                    },
                    {
                        'name': 'MAC',
                        'value': data.mac,
                    },
                    {
                        'name': 'Character',
                        'value': data.name,
                        'inline': True
                    },
                    {
                        'name': 'Class',
                        'value': data.job,
                        'inline': True
                    }
                ]
            }]
        )

        user = User(unique=data.unique, mac=data.mac)

    # New character
    if not character:
        character = Character(
            serverId=data.serverId,
            playerId=data.playerId,
            name=data.name,
            job=data.job
        )
        character.put()

    if not filter(lambda key: character.key == key, user.characters):
        user.characters.append(character.key)

    user.put()
    Logger.insert(data)
    return success_jsonify({
        'success': True
})
