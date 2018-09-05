from __future__ import unicode_literals
from flask import current_app
import flask.json

def safe_jsonify(*args, **kwargs):
  separators = (',', ':')

  if args and kwargs:
    raise TypeError(
        'jsonify() behavior undefined when passed both args and kwargs'
    )
  elif len(args) == 1:
    data = args[0]
  else:
    data = args or kwargs

  dumps_data = flask.json.htmlsafe_dumps(
      data, indent=None, separators=separators
  ).replace(u'+', u'\\u002b')
  return current_app.response_class(
      (dumps_data, '\n'), mimetype='application/json'
  )

def success_jsonify(*args, **kwargs):
  response = safe_jsonify(*args)
  response.status_code = kwargs['code'] if 'code' in kwargs else 200
  return response

def error_jsonify(*args, **kwargs):
  response = safe_jsonify(*args)
  response.status_code = kwargs['code'] if 'code' in kwargs else 500
  return response
