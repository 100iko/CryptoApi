from flask_restful import Resource, reqparse, fields, marshal_with

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
