import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    accel_df = pd.read_csv('accelerometer_data.csv')
    gyro_df = pd.read_csv('gyroscope_data.csv')
    print("Both accelerometer and gyroscope CSV files loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: Could not find a CSV file. Make sure both files are in the same folder. Details: {e}")
    exit()

accel_df['timestamp'] = pd.to_datetime(accel_df['timestamp'])
gyro_df['timestamp'] = pd.to_datetime(gyro_df['timestamp'])

fig = make_subplots(rows=2, cols=1,
                    shared_xaxes=True,
                    subplot_titles=('Accelerometer (Orientation)', 'Gyroscope (Rotation Speed)'))

fig.add_trace(go.Scatter(x=accel_df['timestamp'], y=accel_df['x'], name='Accel X'), row=1, col=1)
fig.add_trace(go.Scatter(x=accel_df['timestamp'], y=accel_df['y'], name='Accel Y'), row=1, col=1)
fig.add_trace(go.Scatter(x=accel_df['timestamp'], y=accel_df['z'], name='Accel Z'), row=1, col=1)

fig.add_trace(go.Scatter(x=gyro_df['timestamp'], y=gyro_df['x'], name='Gyro X'), row=2, col=1)
fig.add_trace(go.Scatter(x=gyro_df['timestamp'], y=gyro_df['y'], name='Gyro Y'), row=2, col=1)
fig.add_trace(go.Scatter(x=gyro_df['timestamp'], y=gyro_df['z'], name='Gyro Z'), row=2, col=1)

fig.update_layout(title_text='Combined Accelerometer and Gyroscope Data for Salat')
fig.write_html("combined_sensor_plot.html")

print("\nPlot saved successfully!")
print("Look for 'combined_sensor_plot.html' in your project folder.")