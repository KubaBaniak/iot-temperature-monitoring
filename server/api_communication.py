import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def get_data() -> pd.DataFrame:
    hostname = os.getenv("HOSTNAME")
    port = os.getenv("PORT")
    auth_token = os.getenv("AUTH_TOKEN")
    entity_type = os.getenv("ENTITY_TYPE")
    device_id = os.getenv("DEVICE_ID")

    default_start_ts = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
    default_end_ts = int(datetime.now().timestamp() * 1000)

    start_ts = int(os.getenv("START_TIMESTAMP", default_start_ts))
    end_ts = int(os.getenv("END_TIMESTAMP", default_end_ts))

    query = f"keys=temperature&startTs={start_ts}&endTs={end_ts}&limit=1500"
    url = f"http://{hostname}:{port}/api/plugins/telemetry/{entity_type}/{device_id}/values/timeseries?{query}"
    headers = {'Content-Type': 'application/json', 'X-Authorization': f"{auth_token}"}

    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        temperature_data = data.get('temperature', [])
        df = pd.DataFrame(temperature_data)
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['value'] = df['value'].astype(float)
        df = df.rename(columns={'ts': 'timestamp', 'value': 'temperature'})

        df.set_index('timestamp', inplace=True)
        df = df.resample('10min').mean()
        df['temperature'] = df['temperature'].interpolate(method='linear')
        df.reset_index(inplace=True)

        return df
    except ValueError:
        print("Response is not JSON")
        return pd.DataFrame()
