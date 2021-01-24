from flask import Flask
from flask_restful import Api

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from resources import CandleList

app = Flask(__name__)
app.config.from_pyfile('app.cfg', True)

api = Api(app)

api.add_resource(CandleList, '/candles/<string:pair>')


@app.before_first_request
def create_tables():
    db.create_all()


def scrap_kraken():
    curr_time = time.strftime("%A, %d. %B %Y %I:%M:%S %p")
    print(f"Kraken Cron Pass: {curr_time}")

    with app.app_context():
        CandleList.scrap_kraken('XETHZEUR')


def setup_cron():
    cron = BackgroundScheduler()

    cron.add_job(func=scrap_kraken, trigger=CronTrigger(hour="*/3"))
    cron.start()

    atexit.register(lambda: cron.shutdown())


if __name__ == '__main__':
    from db import db

    db.init_app(app)
    setup_cron()

    app.run(debug=True)

# lsof -ti:5000 | xargs kill -9
