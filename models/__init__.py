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
    'XLTCZUSD': EthBtc,

    'LTCBTC': LtcBtc,
    'XLTCXXBT': LtcBtc,

    'LTCETH': LtcEth
}
