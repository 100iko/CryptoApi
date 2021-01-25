from flask_apscheduler import APScheduler

from .jobs import scrap_kraken

scheduler = APScheduler()


@scheduler.task('cron', second='0', minute='0', hour='*/3')
def job_scrap_kraken_btc_usd():
    with scheduler.app.app_context():
        scrap_kraken('XXBTZUSD')


@scheduler.task('cron', second='10', minute='0', hour='*/3')
def job_scrap_kraken_etg_usd():
    with scheduler.app.app_context():
        scrap_kraken('XETHZUSD')


@scheduler.task('cron', second='20', minute='0', hour='*/3')
def job_scrap_kraken_ltc_usd():
    with scheduler.app.app_context():
        scrap_kraken('XLTCZUSD')


@scheduler.task('cron', second='30', minute='0', hour='*/3')
def job_scrap_kraken_eth_btc():
    with scheduler.app.app_context():
        scrap_kraken('XETHXXBT')


@scheduler.task('cron', second='40', minute='0', hour='*/3')
def job_scrap_kraken_ltc_btc():
    with scheduler.app.app_context():
        scrap_kraken('XLTCXXBT')


@scheduler.task('cron', second='50', minute='0', hour='*/3')
def job_scrap_kraken_ltc_eth():
    with scheduler.app.app_context():
        scrap_kraken('LTCETH')
