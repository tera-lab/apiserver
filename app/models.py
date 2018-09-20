# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime
from google.appengine.ext import ndb
from bigquery import get_client


class Cosplay(ndb.Model):
    name = ndb.StringProperty()
    preset = ndb.JsonProperty()
    updated_at = ndb.DateTimeProperty(auto_now_add=True)

class Character(ndb.Model):
    serverId = ndb.IntegerProperty()
    playerId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    job = ndb.StringProperty()

class User(ndb.Model):
    unique = ndb.StringProperty()
    mac = ndb.StringProperty()
    characters = ndb.KeyProperty(kind=Character, repeated=True)

class Logger():
    def __init__(self):
        self._cli = get_client(json_key_file='misc/tera-lab.json')

    def insert(self, data):
        data.timestamp = datetime.now()
        self._cli.push_rows('login_log', 'raw', [data])
