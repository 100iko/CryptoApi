from flask_apscheduler import APScheduler
import atexit

from .jobs import scrap_kraken

scheduler = APScheduler()

atexit.register(lambda: scheduler.shutdown())


@scheduler.task('cron', minute='0', hour="*/4")
def job_scrap_kraken_btc_usd():
    with scheduler.app.app_context():
        scrap_kraken('XXBTZUSD')


@scheduler.task('cron', minute='1', hour="*/4")
def job_scrap_kraken_etg_usd():
    with scheduler.app.app_context():
        scrap_kraken('XETHZUSD')


@scheduler.task('cron', minute='2', hour="*/4")
def job_scrap_kraken_ltc_usd():
    with scheduler.app.app_context():
        scrap_kraken('XLTCZUSD')


@scheduler.task('cron', minute='3', hour="*/4")
def job_scrap_kraken_eth_btc():
    with scheduler.app.app_context():
        scrap_kraken('XETHXXBT')


@scheduler.task('cron', minute='4', hour="*/4")
def job_scrap_kraken_ltc_btc():
    with scheduler.app.app_context():
        scrap_kraken('XLTCXXBT')


@scheduler.task('cron', minute='5', hour="*/4")
def job_scrap_kraken_ltc_eth():
    with scheduler.app.app_context():
        scrap_kraken('LTCETH')
