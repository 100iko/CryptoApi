from flask_restful import Resource, reqparse, fields, marshal_with, abort

from models import candle_pairs

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
        self.reqparse.add_argument('limit', type=int, default=10, location="args")
        self.reqparse.add_argument('offset', type=int, default=0, location="args")
        super(CandleList, self).__init__()

    @marshal_with(candle_fields)
    def get(self, pair):
        if pair is candle_pairs.keys():
            abort(400)

        args = self.reqparse.parse_args()

        candle_type = candle_pairs[pair]

        return candle_type.query.order_by(candle_type.time.desc()).offset(args['offset']).limit(
            args['limit']).all(), 200
