from flask_restful import Resource, reqparse, fields, marshal, abort

from models import candle_pairs

candles_format = {
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
        self.reqparse.add_argument('limit', type=int, default=10, location="args")
        self.reqparse.add_argument('offset', type=int, default=0, location="args")
        super(CandleList, self).__init__()

    def get(self, pair: str):
        pair = pair.upper()

        if pair is candle_pairs.keys():
            abort(400)

        args = self.reqparse.parse_args()

        candle_type = candle_pairs[pair]

        count: int = candle_type.query.count()

        first: int = candle_type.query.order_by(candle_type.time.asc()).first().time
        last: int = candle_type.query.order_by(candle_type.time.desc()).first().time
        expected: int = int((last - first) / 60) + 1

        missing_data = count != expected

        data = candle_type.query.order_by(candle_type.time.desc()).offset(args['offset']).limit(
            args['limit']).all()

        return {'result': {
            'info': {
                'count': count,
                'missing_candles': missing_data
            },
            'data': marshal(data, candles_format)
        }}, 200
