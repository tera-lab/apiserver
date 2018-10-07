# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime, timedelta
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

    def to_list(self):
        return {
            'serverId': self.serverId,
            'playerId': self.playerId,
            'name': self.name,
            'job': self.job,
        }


class User(ndb.Model):
    unique = ndb.StringProperty()
    mac = ndb.StringProperty()
    characters = ndb.KeyProperty(kind=Character, repeated=True)
    mods = ndb.StringProperty(repeated=True)

    def to_list(self):
        return {
            'unique': self.unique,
            'mac': self.mac,
            'characters': [key.get().to_list() for key in self.characters],
            'mods': self.mods
        }


class Logger():
    _cli = get_client(json_key_file='misc/tera-lab.json', readonly=False)

    @classmethod
    def insert(self, data):
        import os
        if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._cli.push_rows('log', 'login', [data])
