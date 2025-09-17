import websocket
import json
import csv
from datetime import datetime

CSV_FILE_PATH = 'gyroscope_data.csv'
csv_file = open(CSV_FILE_PATH, 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['timestamp', 'x', 'y', 'z'])
print(f"Ready to write gyroscope data to {CSV_FILE_PATH}")

def on_message(ws, message):
    try:
        data = json.loads(message)
        values = data['values']
        timestamp = datetime.now().isoformat()
        x, y, z = values[0], values[1], values[2]
        csv_writer.writerow([timestamp, x, y, z])
    except Exception as e:
        print(f"Gyro Error: {e}")

def on_error(ws, error):
    print(f"Gyro Error: {error}")
    
def on_close(ws, close_code, reason):
    csv_file.close()
    print("Gyroscope collection stopped.")
    
def on_open(ws):
    print("Gyroscope connection opened.")

def connect(url):
    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    try:
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()

GYRO_URL = "ws://192.168.68.103:8080/sensor/connect?type=android.sensor.gyroscope"
connect(GYRO_URL)