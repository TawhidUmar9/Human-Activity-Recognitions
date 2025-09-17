# Human Activity Recognition (Salat Tracking)

This project focuses on collecting and analyzing **smartphone sensor data** to recognize prayer postures (Salat) such as **Qiyam (standing), Ruku (bowing), Sujud (prostration), and Jalsa (sitting)**.  
The ultimate goal is to identify patterns in sensor signals that can distinguish postures and detect whether the prayer is performed **slowly or quickly**.

# Data Collection

Sensor data is collected using the [SensorServer](https://github.com/umer0586/SensorServer) Android application.  
The app streams or logs raw data from the following smartphone sensors:

- Accelerometer (x, y, z)
- Gyroscope (x, y, z)

Finally the data is visualized as plots.
