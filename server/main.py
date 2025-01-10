import os
from dotenv import load_dotenv
from data_utils import generate_december_data, load_test_data
from prediction import predict_temperature_tbats, plot_temperature_and_prediction_tbats
from api_communication import get_data

load_dotenv()


def main():
    mode = os.getenv("MODE", "dev")
    test_file = "data/test_data.csv"

    print(f"Running in {mode.upper()} mode...")

    if mode == "dev":
        print('---GENERATING TEST DATA---')
        generate_december_data(test_file)

        print('---LOADING TEST DATA---')
        historical_data = load_test_data(test_file)

    elif mode == "prod":
        print('---FETCHING REAL DATA FROM API---')
        historical_data = get_data()

    else:
        raise ValueError(f"Invalid MODE: {mode}. Expected 'dev' or 'prod'.")

    if not historical_data.empty:
        print(f"Retrieved {len(historical_data)} historical records.")

        print('---PREDICTING FUTURE TEMPERATURES---')
        hours_to_predict = 24
        predictions = predict_temperature_tbats(historical_data, hours=hours_to_predict)
        print(f"Predicted Temperatures for next {hours_to_predict} hours:", predictions)

        print('---PLOTTING DATA---')
        plot_temperature_and_prediction_tbats(historical_data, predictions, hours=hours_to_predict)
    else:
        print("No historical data retrieved.")


if __name__ == "__main__":
    main()
