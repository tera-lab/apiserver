# coding: utf-8
from flask import Flask

app = Flask(__name__)

from api import api as api_blueprint
from response import error_jsonify
app.register_blueprint(api_blueprint)


@app.errorhandler(500)
def internal_error(e):
    return error_jsonify({'error': 'エラーが発生しました'})
