# coding: utf-8
from __future__ import unicode_literals
from . import api
from ..response import error_jsonify
from ..exceptions import *


@api.errorhandler(OutOfTimeException)
def out_of_time(e):
    return error_jsonify({'error': 'out of time'})


@api.errorhandler(UserNotFound)
def user_notfound(e):
    return error_jsonify({'error': 'user not found'}, code=404)


@api.errorhandler(CharacterNotFound)
def character_notfound(e):
    return error_jsonify({'error': 'character not found'}, code=404)


@api.errorhandler(ServerUnknown)
def server_unknown(e):
    return error_jsonify({'error': 'server unknown'})


@api.errorhandler(NotifyTypeUnknown)
def notifytype_unknown(e):
    return error_jsonify({'error': 'notify_type unknown'})
