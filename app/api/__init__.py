# coding: utf-8
from __future__ import unicode_literals
from flask import Blueprint
from flask_cors import CORS

api = Blueprint('api', __name__)
CORS(api)

from . import cosplay
from . import guild_bam
from . import lfg

from . import errors

@api.route('/')
def index():
  return 'ok'
