import requests
import pandas as pd

# Binance API URL
url = "https://api.binance.com/api/v3/klines"

# Trading pair and interval (e.g., BTCUSDT, 1h)
symbol = "BTCUSDT"
interval = "1h"

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
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Save the data to a CSV file
csv_filename = f"{symbol}_{interval}_data.csv"
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
