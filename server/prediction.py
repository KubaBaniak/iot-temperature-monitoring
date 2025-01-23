import pandas as pd
import matplotlib.pyplot as plt
from tbats import TBATS

def predict_temperature_tbats(data: pd.DataFrame, hours: int = 3) -> list:
    steps = hours * 6
    temperatures = data['temperature']

    estimator = TBATS(seasonal_periods=[144])  # 144 = daily seasonality (10-minute intervals)
    model = estimator.fit(temperatures)
    forecast = model.forecast(steps=steps)
    return forecast.tolist()

def plot_temperature_and_prediction_tbats(data: pd.DataFrame, predictions: list, hours: int = 3) -> None:
    steps = hours * 6
    last_24h_data = data.tail(6*24*4)
    prediction_timestamps = pd.date_range(start=last_24h_data['timestamp'].iloc[-1], periods=steps + 1, freq="10min")[1:]

    plt.figure(figsize=(12, 6))
    plt.plot(last_24h_data['timestamp'], last_24h_data['temperature'], label='Temperature (Last 24h)')
    plt.plot(prediction_timestamps, predictions, label='Predicted Temperatures (TBATS)', linestyle='--', marker='o')
    plt.title('Temperature in Last 24 Hours and Predictions')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
