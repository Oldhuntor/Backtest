import websocket
import threading
import json
import time
# WebSocket URL
websocket_url = "wss://stream.binance.com:9443/ws"

# List of stream names
stream_names = ["btcusdt@aggTrade", "btcusdt@depth"]

def on_message(ws, message):
    data = json.loads(message)
    print(data)
    # Handle incoming messages

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    # Subscribe to streams
    payload = {
        "method": "SUBSCRIBE",
        "params": stream_names,
        "id": 1
    }
    ws.send(json.dumps(payload))

def start_websocket():
    ws = websocket.WebSocketApp(websocket_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

if __name__ == "__main__":
    # Create a thread for WebSocket connection
    websocket_thread = threading.Thread(target=start_websocket)
    websocket_thread.start()

    # Perform other tasks in the main program
    while True:
        time.sleep(60)
        print("Doing other tasks...")
        # Your other tasks here

    # Wait for the WebSocket thread to finish (optional)
    websocket_thread.join()
