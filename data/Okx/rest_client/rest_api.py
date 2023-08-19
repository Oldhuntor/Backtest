import requests
import pandas as pd
import time

# 设置基本信息
base_url = "https://www.okex.com/api/v5/market/history-index-candles"

def get_data():
    """
    symbol
    frequency
    limit

    """
    params = {
        "instId": inst_id,
        "bar": time_interval,
        "limit": limit
    }
    



inst_id = "BTC-USD"  # 替换为你需要的指数
time_interval = "1H"  # 时间粒度，可以根据需要调整
limit = 100  # 返回的结果集数量

# 创建一个空的 Pandas DataFrame
columns = ["Timestamp", "Open", "High", "Low", "Close", "Confirm"]
data_frame = pd.DataFrame(columns=columns)

# 循环获取历史数据
while True:
    # 构造请求参数
    params = {
        "instId": inst_id,
        "bar": time_interval,
        "limit": limit
    }

    # 发送 GET 请求
    response = requests.get(base_url, params=params)

    # 解析响应数据并添加到 DataFrame
    if response.status_code == 200:
        data = response.json().get("data")
        if data:
            for item in data:
                data_frame = data_frame.append(pd.Series(item, index=columns), ignore_index=True)
    else:
        print(f"Error: {response.status_code}")

    # 限速，每次请求后休眠一段时间
    time.sleep(2)  # 每次请求间隔 2 秒

    # 退出循环条件（示例中为获取10次数据后退出）
    if len(data_frame) >= 1000:  # 假设获取 1000 条数据后退出循环
        break


