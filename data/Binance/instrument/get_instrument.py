import requests
import pandas as pd
import os

path = os.getcwd()


FuturesUmUrl = "https://fapi.binance.com/fapi/v1/exchangeInfo"
FuturesCmUrl = "https://dapi.binance.com/dapi/v1/exchangeInfo"
SpotUrl = "https://api.binance.com/api/v3/exchangeInfo"

def get_instruments(type):
    """
    type : "Um","Cm","Spot"
    return : list
    """
    if type == "Um":
        url = FuturesUmUrl
    elif type == "Cm":
        url = FuturesCmUrl
    else:
        url = SpotUrl

    response = requests.get(url)
    # 解析响应数据
    symbolist = []
    if response.status_code == 200:
        exchange_info = response.json()
        symbols = [symbol_info['symbol'] for symbol_info in exchange_info['symbols']]
        for symbol in symbols:
            symbolist.append(symbol)
        return symbolist
    else:
        print(f"Error: {response.status_code}")
        return False

if __name__ == '__main__':
    spot = get_instruments("Spot")
    um = get_instruments("Um")
    cm = get_instruments("Cm")
    # 确保所有列的长度相同，如果长度不足，使用 None 来填充
    max_length = max(len(spot), len(um), len(cm))
    spot += [None] * (max_length - len(spot))
    um += [None] * (max_length - len(um))
    cm += [None] * (max_length - len(cm))
    data = {
        "Spot":spot,
        "Um":um,
        "Cm":cm,
    }

    data = pd.DataFrame(data)
    data.to_csv(path +'/instruments.csv')