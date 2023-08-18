import requests
import pandas as pd
import sqlite3
from data.database.sqlite_server import connectSqlite, DBpath


# Binance API URL
url = "https://api.binance.com/api/v3/klines"

# Trading pair and interval (e.g., BTCUSDT, 1h)
symbol = "BTCUSDT"
interval = "1m"

# read the time of the last data
table_name = f"{symbol}_{interval}"
conn = connectSqlite(DBpath)
cursor = conn.cursor()

try:
# executing query
    query = f"SELECT * FROM {table_name} ORDER BY timestamp DESC LIMIT 1;"
    cursor.execute(query)
    last_row = cursor.fetchone()
    last_timestamp = last_row[0]
    cursor.close()
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1000,  # Number of data points to retrieve
        "startTime": last_timestamp
    }

except Exception as e:
    print(e)
    # Request parameters
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": 1000,  # Number of data points to retrieve
    }

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Convert the response data to a Pandas DataFrame
columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
df = pd.DataFrame(data, columns=columns)

# Convert timestamp to datetime format
df["time"] = pd.to_datetime(df["timestamp"], unit="ms")

# Save the data to a CSV file
print(table_name)
print(df)
df.to_sql(table_name, conn, if_exists='append', index=False)
# Close the connection
conn.close()
