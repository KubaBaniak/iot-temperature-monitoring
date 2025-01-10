import pandas as pd
import random
import numpy as np

def generate_december_data(file_path: str) -> None:
    timestamps = pd.date_range(start="2024-12-01 00:00:00", end="2024-12-07 23:59:59", freq="10min")
    temperatures = []

    for ts in timestamps:
        hour = ts.hour
        daily_variation = 2 * np.sin(2 * np.pi * (hour - 6) / 24)
        base_temp = 20.0
        noise = random.uniform(-0.2, 0.2)
        temperatures.append(base_temp + daily_variation + noise)

    temperatures = pd.Series(temperatures).rolling(window=6, min_periods=1, center=True).mean()

    for _ in range(100):
        index_to_null = random.randint(0, len(temperatures) - 1)
        temperatures.iloc[index_to_null] = None

    december_data = pd.DataFrame({
        "timestamp": timestamps,
        "temperature": temperatures
    })

    december_data.to_csv(file_path, index=False)
    print(f"December data generated and saved to {file_path}")

def load_test_data(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)
        df = df.resample('10min').mean()
        df['temperature'] = df['temperature'].interpolate(method='linear')
        df.reset_index(inplace=True)
        return df
    except Exception as e:
        print(f"Error loading test data: {e}")
        return pd.DataFrame()
