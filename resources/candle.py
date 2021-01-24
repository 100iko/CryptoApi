from flask_restful import Resource, reqparse, fields, marshal_with
import requests

from models import CandleModel

candle_fields = {
    'time': fields.Integer,
    'open': fields.Float,
    'high': fields.Float,
    'low': fields.Float,
    'close': fields.Float,
    'vwap': fields.Float,
    'volume': fields.Float,
    'count': fields.Integer,
}


class CandleList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('interval', type=int, default=1, location="args")
        super(CandleList, self).__init__()

    @marshal_with(candle_fields)
    def get(self, pair):
        args = self.reqparse.parse_args()
        return [item for item in CandleModel.query.all()], 200

    @staticmethod
    def scrap_kraken(pair: str, interval: int = 1):
        url = "https://api.kraken.com/0/public/OHLC"
        params = {'pair': pair, 'interval': interval}

        response = requests.get(url, params).json()

        result = response['result']
        data: map = result[pair]
        last: int = result['last']

        if data[-1][0] > last: data.pop(-1)

        candles = [CandleModel(*i) for i in data]

        for candle in candles:
            if not CandleModel.find_by_time(candle.time):
                candle.save_to_db()
