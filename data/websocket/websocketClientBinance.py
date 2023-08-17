import websocket
import json
import time

# WebSocket URL
websocket_url = "wss://stream.binance.com:9443/ws"

# List of stream names
stream_names = ["btcusdt@aggTrade", "btcusdt@depth"]

def on_message(ws, message):
    data = json.loads(message)
    # print(data)
    # Handle incoming messages


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("Closed")
    # Automatically reconnect
    while True:
        try:
            print("Reconnecting...")
            time.sleep(5)  # Wait before reconnecting
            ws.connect(websocket_url)
            print("Reconnected!")
            break
        except Exception as e:
            print(f"Reconnection error: {e}")


def on_open(ws):
    # Subscribe to streams
    payload = {
        "method": "SUBSCRIBE",
        "params": stream_names,
        "id": 1
    }
    ws.send(json.dumps(payload))


if __name__ == "__main__":
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.on_open = on_open
    ws.run_forever()
