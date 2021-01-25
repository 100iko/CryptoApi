from flask_restful import Api
from .candle import CandleList

api = Api()

api.add_resource(CandleList, '/candles/<string:pair>')
