from db import db


class CandleModel(db.Model):
    __abstract__ = True

    time = db.Column(db.Integer, primary_key=True)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    vwap = db.Column(db.Float)
    volume = db.Column(db.Float)
    count = db.Column(db.Integer)

    def __init__(self, *args):
        self.time = int(args[0])
        self.open = float(args[1])
        self.high = float(args[2])
        self.low = float(args[3])
        self.close = float(args[4])
        self.vwap = float(args[5])
        self.volume = float(args[6])
        self.count = int(args[7])

    def __repr__(self):
        return f"<Candle(Time={self.time}, " \
               f"Open={self.open}, High={self.high}, Low={self.low}, Close={self.close}, " \
               f"Vwap={self.vwap}, Volume={self.volume}, Count={self.count})>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self):
        db.session.merge(self)
        db.session.commit()

    @classmethod
    def find_by_time(cls, time: int):
        return cls.query.filter_by(time=time).first()


class BtcUsd(CandleModel):
    pass


class EthUsd(CandleModel):
    pass


class LtcUsd(CandleModel):
    pass


class EthBtc(CandleModel):
    pass


class LtcBtc(CandleModel):
    pass


class LtcEth(CandleModel):
    pass
