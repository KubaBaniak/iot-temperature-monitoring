# Temperature Monitoring and Forecasting System

## Overview
This project integrates ESP8266, Raspberry Pi, and Docker to collect, store, and forecast temperature data. The system operates in two modes: 
- **Development (dev)**: Uses synthetic test data for forecasting.
- **Production (prod)**: Fetches real temperature data from a ThingsBoard server.

The ESP8266 device transmits temperature data to a server running on Raspberry Pi. The server processes this data and predicts future temperatures using TBATS time series models.

---

## Project Structure

```
project-root/
├── arduino/
│   ├── esp8266_temperature_sender.ino   # Code for ESP8266
│   ├── secrets.h                        # WiFi and server credentials (ignored in Git)
│   └── secrets_example.h                # Template for secrets.h
├── server/
│   ├── main.py                          # Main entry point of the server
│   ├── docker-compose.yml               # Docker configuration for ThingsBoard
│   ├── .env                             # Environment configuration
│   ├── .example.env                     # Template for environment variables
│   ├── api_communication.py             # Functions to communicate with the ThingsBoard API
│   ├── prediction.py                    # Functions for forecasting and plotting
│   ├── data_utils.py                    # Utilities for generating and loading data
│   └── data/
│       └── test_data.csv                # Test data for dev mode (ignored in production)
└── .gitignore                           # Files and directories to be ignored by Git
```

---

## Features

- **Data Collection**: ESP8266 captures temperature readings and sends them to the ThingsBoard server.
- **Data Storage**: Dockerized ThingsBoard stores telemetry data.
- **Temperature Forecasting**: Predicts temperatures for the next 24 hours using TBATS models.
- **Visualization**: Displays historical data and predictions.
- **Dual Mode Operation**: 
  - Development: Uses generated test data.
  - Production: Fetches real data from ThingsBoard.

---

## Setup Instructions

### Prerequisites
- **Hardware**: Raspberry Pi, ESP8266
- **Software**: Docker, Docker Compose, Python 3.9+, Arduino IDE

### Steps

#### Clone the Repository
```bash
git clone <repository-url>
cd project-root
```

#### Set Up ESP8266
1. Open `arduino/esp8266_temperature_sender.ino` in Arduino IDE.
2. Configure `secrets.h` for WiFi and server credentials (see below).
3. Upload the code to ESP8266.

#### Set Up the Server
1. Navigate to the `server/` directory.
2. Configure ThingsBoard using `docker-compose.yml`:
   ```bash
   docker-compose up -d
   ```
3. Ensure ThingsBoard is running at `http://<raspberry-pi-ip>:8080`.

#### Configure Python Environment
1. Create a virtual environment to isolate dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Upgrade `pip`:
   ```bash
   pip install --upgrade pip
   ```

#### Configure Environment Variables
1. Create a `.env` file in the `server/` directory based on `.example.env`:
   ```bash
   cp .example.env .env
   ```
2. Update `.env` with your settings for `MODE` (dev/prod), ThingsBoard host, port, and credentials.

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Run the Server
```bash
python main.py
```

---

## Environment Variables

The project uses a `.env` file to manage configuration:
- **MODE**: `dev` for development, `prod` for production.
- **HOSTNAME**, **PORT**, **AUTH_TOKEN**, **ENTITY_TYPE**, **DEVICE_ID**: ThingsBoard connection details.

For more information, refer to the `.example.env` template.

---

## Setting Up Secrets

1. **Create a Secrets File**:
   - Copy the `secrets_example.h` file to `secrets.h`:
     ```bash
     cp arduino/secrets_example.h arduino/secrets.h
     ```

2. **Edit the Secrets File**:
   - Open `arduino/secrets.h` and fill in your WiFi credentials and server details:
     ```cpp
     const char* ssid = "your-ssid";
     const char* password = "your-password";
     const char* serverName = "http://<your-server-address>/api/v1/<your-access-token>/telemetry";
     ```

3. **Secure the Secrets**:
   - Ensure `secrets.h` is ignored by Git to prevent it from being committed:
     ```bash
     echo "arduino/secrets.h" >> .gitignore
     ```

---

## Running Modes

### Development (dev)
- **Purpose**: Test the system using synthetic data.
- **How**: Generates and processes data stored in `data/test_data.csv`.

### Production (prod)
- **Purpose**: Fetch and process real temperature data from ThingsBoard.
- **How**: Uses API credentials from the `.env` file.

---

## Future Enhancements

- Add real-time data monitoring.
- Enhance error handling and logging.
- Implement CI/CD pipelines for deployment.
- Develop unit tests for all modules.

---

Feel free to suggest edits or ask for additional details!

