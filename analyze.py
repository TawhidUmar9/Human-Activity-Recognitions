import os
import pandas as pd
from pandas.errors import EmptyDataError
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ACCEL_PATH = 'accelerometer_data.csv'
GYRO_PATH = 'gyroscope_data.csv'


def safe_read_csv(path: str) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        print(f"Warning: {path} not found. Proceeding with empty dataframe.")
        return pd.DataFrame(columns=['timestamp', 'x', 'y', 'z'])
    except EmptyDataError:
        print(f"Warning: {path} is empty. Proceeding with empty dataframe.")
        return pd.DataFrame(columns=['timestamp', 'x', 'y', 'z'])


accel_df = safe_read_csv(ACCEL_PATH)
gyro_df = safe_read_csv(GYRO_PATH)

if not accel_df.empty and 'timestamp' in accel_df.columns:
    accel_df['timestamp'] = pd.to_datetime(accel_df['timestamp'], errors='coerce')
if not gyro_df.empty and 'timestamp' in gyro_df.columns:
    gyro_df['timestamp'] = pd.to_datetime(gyro_df['timestamp'], errors='coerce')

fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    subplot_titles=('Accelerometer (Orientation)', 'Gyroscope (Rotation Speed)'))

# Accelerometer traces
if not accel_df.empty:
    fig.add_trace(go.Scatter(x=accel_df['timestamp'], y=accel_df['x'], name='Accel X'), row=1, col=1)
    fig.add_trace(go.Scatter(x=accel_df['timestamp'], y=accel_df['y'], name='Accel Y'), row=1, col=1)
    fig.add_trace(go.Scatter(x=accel_df['timestamp'], y=accel_df['z'], name='Accel Z'), row=1, col=1)
else:
    fig.add_trace(go.Scatter(x=[], y=[], name='Accel X (no data)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=[], y=[], name='Accel Y (no data)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=[], y=[], name='Accel Z (no data)'), row=1, col=1)

# Gyroscope traces
if not gyro_df.empty:
    fig.add_trace(go.Scatter(x=gyro_df['timestamp'], y=gyro_df['x'], name='Gyro X'), row=2, col=1)
    fig.add_trace(go.Scatter(x=gyro_df['timestamp'], y=gyro_df['y'], name='Gyro Y'), row=2, col=1)
    fig.add_trace(go.Scatter(x=gyro_df['timestamp'], y=gyro_df['z'], name='Gyro Z'), row=2, col=1)
else:
    fig.add_trace(go.Scatter(x=[], y=[], name='Gyro X (no data)'), row=2, col=1)
    fig.add_trace(go.Scatter(x=[], y=[], name='Gyro Y (no data)'), row=2, col=1)
    fig.add_trace(go.Scatter(x=[], y=[], name='Gyro Z (no data)'), row=2, col=1)

fig.update_layout(title_text='Combined Accelerometer and Gyroscope Data for Salat')
fig.write_html("combined_sensor_plot.html")

print("\nPlot saved successfully!")
print("Look for 'combined_sensor_plot.html' in your project folder.")