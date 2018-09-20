# coding: utf-8
from __future__ import unicode_literals
from google.appengine.ext import ndb

class Cosplay(ndb.Model):
  name = ndb.StringProperty()
  preset = ndb.JsonProperty()
  updated_at = ndb.DateTimeProperty(auto_now_add=True)
