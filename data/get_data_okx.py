import requests
import pandas as pd
from data.database.sqlite_server import connectSqlite, DBpath

# OKEx API URL
url = "https://www.okex.com/api/spot/v3/instruments/BTC-USDT/candles"

# Trading pair and interval (e.g., BTC-USDT, 1h)
symbol = "BTC-USDT"
interval = "1h"

# Request parameters
params = {
    "granularity": 3600,  # Granularity in seconds (1 hour)
    "start": None,  # Set the start time in ISO 8601 format (e.g., "2023-01-01T00:00:00Z")
    "end": None,    # Set the end time in ISO 8601 format (e.g., "2023-01-31T23:59:59Z")
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Convert the response data to a Pandas DataFrame
columns = ["timestamp", "open", "high", "low", "close", "volume"]
df = pd.DataFrame(data, columns=columns)

# Convert timestamp to datetime format
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

# Save the data to a CSV file
csv_filename = f"{symbol}_{interval}_data.csv"
# Save the data to a CSV file
table_name = f"{symbol}_{interval}"
conn = connectSqlite(DBpath)
print(table_name)
df.to_sql(table_name, conn, if_exists='append', index=False)
# Close the connection
conn.close()
