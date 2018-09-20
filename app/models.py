# coding: utf-8
from __future__ import unicode_literals
from google.appengine.ext import ndb
from bigquery import get_client
import datetime

class Cosplay(ndb.Model):
  name = ndb.StringProperty()
  preset = ndb.JsonProperty()
  updated_at = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
  unique = ndb.StringProperty()
  mac = ndb.StringProperty()
  characters = ndb.JsonProperty()

class Logger():
  def __init__(self):
    self._cli = get_client(json_key_file='misc/tera-lab.json', readonly=True)

  def log(self, data):
    data['timestamp'] = datetime.now()
    self._cli.push_rows('login_log', 'raw', [data]])
