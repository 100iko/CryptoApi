from flask import Blueprint, render_template, abort

from models import candle_pairs

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    abort(404)


@routes.route('/doc')
def documentation():
    return {
               'paths': {
                   '/charts': {},
                   '/candles/<pair>': {'params': {
                       'interval': 'optional, default=1, wip',
                       'limit': 'optional, default=10',
                       'offset': 'optional, default=0'
                   }}
               },
               'pairs': [str(x) for x in candle_pairs.keys()],
           }, 200
