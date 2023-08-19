import requests
from data.database.sqlite_server import connectSqlite, DBpath

FuturesUmUrl = "https://fapi.binance.com/fapi/v1/exchangeInfo"
FuturesCmUrl = "https://dapi.binance.com/dapi/v1/exchangeInfo"
SpotUrl = "https://api.binance.com/api/v3/exchangeInfo"