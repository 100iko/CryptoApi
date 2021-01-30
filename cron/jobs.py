from datetime import datetime
import requests

from models import candle_pairs


def scrap_kraken(pair: str, interval: int = 1):
    print(f"{datetime.utcnow()}: {pair} Cron Pass")

    url = "https://api.kraken.com/0/public/OHLC"
    params = {'pair': pair, 'interval': interval}

    response = requests.get(url, params).json()

    result = response['result']
    data: map = result[pair]
    last: int = result['last']

    if data[-1][0] > last: data.pop(-1)

    candle_type = candle_pairs[pair]

    candles = [candle_type(*i) for i in data]

    for candle in candles:
        if candle_type.find_by_time(candle.time):
            if len({candle.open, candle.high, candle.close, candle.low}) > 1:
                candle.update_to_db()
        else:
            candle.save_to_db()
