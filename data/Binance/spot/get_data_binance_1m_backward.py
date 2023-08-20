import requests
import pandas as pd
import sqlite3
from data.database.sqlite_server import connectSqlite, DBpath


"""
Make a for loop to get all the historical data until we reach the end
"""


# Binance API URL
url = "https://api.binance.com/api/v3/klines"

# Trading pair and interval (e.g., BTCUSDT, 1h)
symbol = "BTCUSDT"
interval = "1m"
exchange = "binance"
# read the time of the last data
table_name = f"{exchange}_{symbol}_{interval}"
conn = connectSqlite(DBpath)
cursor = conn.cursor()

# find the earliest timestamp
try:
    query = f"SELECT * FROM {table_name} ORDER BY timestamp ASC LIMIT 1;"
    cursor.execute(query)
    first_row = cursor.fetchone()
    first_timestamp = first_row[0]
    cursor.close()
    have_table = True

except Exception as e:
    print(e)
    have_table = False


request_time = 5

if have_table:
    columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
               "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
    df_old = pd.DataFrame(columns=columns)
    endTimeNew = first_timestamp
    for i in range(request_time):

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": 1000,  # Number of data points to retrieve
            "endTime": endTimeNew
        }
        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()
        df_new = pd.DataFrame(data, columns=columns)

        endTimeNew = df_new['timestamp'].iloc[0]
        df_old = df_new.append(df_old)

else:
    columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
               "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
    df_old = pd.DataFrame(columns=columns)
    for i in range(request_time):
        if i == 0:
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": 1000,  # Number of data points to retrieve
            }
        else:
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": 1000,  # Number of data points to retrieve
                "endTime":endTimeNew
            }
        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()
        df_new = pd.DataFrame(data, columns=columns)
        endTimeNew = df_new['timestamp'].iloc[0]
        df_old = df_new.append(df_old)


# Save the data to a CSV file
print(table_name)
print(df_old)
# Convert timestamp to datetime format
df_old["time"] = pd.to_datetime(df_old["timestamp"], unit="ms")
df_old.to_sql(table_name, conn, if_exists='append', index=False)
# Close the connection
conn.close()
