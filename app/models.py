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
    _cli = get_client(json_key_file='misc/tera-lab.json', readonly=False)

    @classmethod
    def insert(self, data):
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._cli.push_rows('log', 'login', [data])
