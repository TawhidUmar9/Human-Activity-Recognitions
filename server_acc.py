import websocket
import json
import csv
from datetime import datetime

CSV_FILE_PATH = 'accelerometer_data.csv'
csv_file = open(CSV_FILE_PATH, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'x', 'y', 'z']) 
csv_file.flush()
print(f"Ready to write accelerometer data to {CSV_FILE_PATH}")

def _load_ws_base(path: str = 'address.txt') -> str:
    """Return base ws URL like ws://host:port read from address.txt; fallback to last known address."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            addr = f.read().strip()
            if not addr:
                raise ValueError('address.txt is empty')
            if addr.startswith('ws://') or addr.startswith('wss://'):
                base = addr
            else:
                base = f"ws://{addr}"
            return base.rstrip('/')
    except Exception as e:
        fallback = 'ws://192.168.68.100:8080'
        print(f"Warning: Could not read {path} ({e}). Falling back to {fallback}")
        return fallback

BASE_WS = _load_ws_base()
ACCEL_URL = f"{BASE_WS}/sensor/connect?type=android.sensor.accelerometer"

def on_message(ws, message):
    try:
        data = json.loads(message)
        values = data['values']
        timestamp = datetime.now().isoformat()
        x, y, z = values[0], values[1], values[2]
        csv_writer.writerow([timestamp, x, y, z])
        csv_file.flush()
    except Exception as e:
        print(f"Accel Error: {e}")

def on_error(ws, error):
    print(f"Accel Error: {error}")
    
def on_close(ws, close_code, reason):
    csv_file.close()
    print("Accelerometer collection stopped.")
    
def on_open(ws):
    print("Accelerometer connection opened.")

def connect(url):
    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

connect(ACCEL_URL)