import requests
from data.database.sqlite_server import connectSqlite, DBpath

FuturesUmUrl = "https://fapi.binance.com/fapi/v1/"
FuturesCmUrl = "https://dapi.binance.com/dapi/v1/"
SpotUrl = "https://api.binance.com/api/v3/"



def get_kline(symbol, type, frequency, startTime, endTime ,is_forward, request_time):
    """
    type = 'cm','um','spot'
    symbol:
        spot: BTCUSDT
        um: BTCUSDT
        cm : BTCUSD

    frequency:
        1m,1h,1d

    startTime : 1692474360000
    endTime : 1692474360000
    is_forward : True; False
    path = klines
    """

    if is_forward:
        pass


def get_instrument():
    path = 'exchangeInfo'
    pass


