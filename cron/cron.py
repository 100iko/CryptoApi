from flask_apscheduler import APScheduler
import atexit

from .jobs import scrap_kraken

scheduler = APScheduler()

atexit.register(lambda: scheduler.shutdown())


@scheduler.task('cron', minute='*', hour="*")
def job_scrap_kraken_eth_eur():
    with scheduler.app.app_context():
        scrap_kraken('XETHZUSD')
