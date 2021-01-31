from .candle import BtcUsd
from .candle import EthUsd
from .candle import LtcUsd
from .candle import EthBtc
from .candle import LtcBtc
from .candle import LtcEth

candle_pairs = {
    'BTCUSD': BtcUsd,
    'XXBTZUSD': BtcUsd,

    'ETHUSD': EthUsd,
    'XETHZUSD': EthUsd,

    'LTCUSD': LtcUsd,
    'XLTCZUSD': LtcUsd,

    'ETHBTC': EthBtc,
    'XETHXXBT': EthBtc,

    'LTCBTC': LtcBtc,
    'XLTCXXBT': LtcBtc,

    'LTCETH': LtcEth
}

unique_pairs = {
    'BTCUSD': BtcUsd,
    'ETHUSD': EthUsd,
    'LTCUSD': LtcUsd,
    'ETHBTC': EthBtc,
    'LTCBTC': LtcBtc,
    'LTCETH': LtcEth
}
