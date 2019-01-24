# coding: utf-8
from __future__ import unicode_literals

from datetime import datetime, timedelta
from google.appengine.ext import ndb


class Cosplay(ndb.Model):
    name = ndb.StringProperty()
    preset = ndb.JsonProperty()
    updated_at = ndb.DateTimeProperty(auto_now=True)


class Character(ndb.Model):
    serverId = ndb.IntegerProperty()
    playerId = ndb.IntegerProperty()
    name = ndb.StringProperty()
    job = ndb.StringProperty()
    last_login = ndb.DateTimeProperty(auto_now=True)

    def to_list(self):
        return {
            'serverId': self.serverId,
            'playerId': self.playerId,
            'name': self.name,
            'job': self.job,
        }


class Account(ndb.Model):
    accountId = ndb.IntegerProperty(required=True)
    characters = ndb.StringProperty(repeated=True)


class Mod(ndb.Model):
    name = ndb.StringProperty(required=True)
    raw = ndb.JsonProperty()

    def to_list(self):
        return {'name': self.name, 'raw': self.raw}


class User(ndb.Model):
    unique = ndb.StringProperty()
    mac = ndb.StringProperty()
    characters = ndb.KeyProperty(kind=Character, repeated=True)
    mods = ndb.LocalStructuredProperty(Mod, repeated=True)
    last_login = ndb.DateTimeProperty(auto_now=True)

    def to_list(self):
        return {
            'unique': self.unique,
            'mac': self.mac,
            'characters': [key.get().to_list() for key in self.characters],
            'mods': [mod.to_list() for mod in self.mods]
        }
