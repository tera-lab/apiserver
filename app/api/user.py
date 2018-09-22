# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..models import Character, User, Logger
from ..response import success_jsonify
from ..utils import post_json

from flask import request
from google.appengine.ext import ndb

WEBHOOK = 'https://discordapp.com/api/webhooks/492357190259310603/mS7liQAUsqVUw_Y_7Hsq5klrGfFhv5tvSNOiRLBqeuNyHfajyX8H_5yYk62FuhHrUnmn'


@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query(User.unique == data['unique']).get()
    character = Character.query(
        ndb.AND(
            Character.serverId == data['serverId'],
            Character.playerId == data['playerId']
        )
    ).get()

    # New character
    if not character:
        character = Character(
            serverId=data['serverId'],
            playerId=data['playerId'],
            name=data['name'],
            job=data['job']
        )
    character.put()

    if user:
        if user.mac != data['mac']:
            post_json(
                WEBHOOK, {
                    'username':
                        'Warning',
                    'content':
                        '<@&479964532949778432>',
                    'embeds':
                        [
                            {
                                'title':
                                    ':warning:Unique / MAC mismatch!',
                                'color':
                                    0xff4757,
                                'fields':
                                    [
                                        {
                                            'name':
                                                'Character',
                                            'value':
                                                '{}({})'.format(
                                                    character.name,
                                                    character.job
                                                )
                                        },
                                        {
                                            'name': 'Unique',
                                            'value': user.unique
                                        },
                                        {
                                            'name': 'Registered MAC',
                                            'value': user.mac,
                                            'inline': True
                                        },
                                        {
                                            'name': 'Detected Mac',
                                            'value': data['mac'],
                                            'inline': True
                                        }
                                    ]
                            }
                        ]
                }
            )
    else:
        user = User(unique=data['unique'], mac=data['mac'])
        post_json(
            WEBHOOK, {
                'username':
                    'Information',
                'embeds':
                    [
                        {
                            'title':
                                ':ghost:New User',
                            'color':
                                0x1e90ff,
                            'fields':
                                [
                                    {
                                        'name':
                                            'Character',
                                        'value':
                                            '{}({})'.format(
                                                character.name, character.job
                                            )
                                    },
                                    {
                                        'name': 'Unique',
                                        'value': user.unique,
                                        'inline': True
                                    },
                                    {
                                        'name': 'MAC',
                                        'value': user.mac,
                                        'inline': True
                                    }
                                ]
                        }
                    ]
            }
        )

    if not filter(lambda key: character.key == key, user.characters):
        user.characters.append(character.key)

    user.put()
    Logger.insert(data)
    return success_jsonify({'success': 'logged in'})


@api.route('/user/<unique>/characters', methods=['GET'])
def list_characters(unique):
    user = User.query(User.unique == unique).get()
    characters = [key.get().to_list()
                  for key in user.characters] if user else []

    return success_jsonify({'characters': characters})
