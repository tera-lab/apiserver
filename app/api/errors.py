# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import error_jsonify
from ..exceptions import *


@api.errorhandler(OutOfTimeException)
def out_of_time(e):
    return error_jsonify({'error': 'out of time'})

@api.errorhandler(UserNotFound)
def funcname(e):
    return error_jsonify({'error': 'user not found'})

@api.errorhandler(CharacterNotFound)
def funcname(e):
    return error_jsonify({'error': 'character not found'})
