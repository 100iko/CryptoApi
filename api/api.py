from flask_restful import Api
from .candle import CandleList, CandlesCount

api = Api()

api.add_resource(CandleList, '/candles/<string:pair>')
api.add_resource(CandlesCount, '/candles/<string:pair>/count')
