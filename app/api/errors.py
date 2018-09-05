# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import error_jsonify
from ..exceptions import *

@api.errorhandler(AlreadyNoticedException)
def already_noticed(e):
  return error_jsonify({
    'error': 'already noticed'
  })

@api.errorhandler(OutOfTimeException)
def out_of_time(e):
  return error_jsonify({
    'error': 'out of time'
  })
