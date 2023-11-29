import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from fasttrader import Data

def main():
    print("Welcome to the Stock Price Data Retrieval Tool!")

    # Ask the user for input
    ticker = input("Enter the stock ticker symbol (e.g., AAPL): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    interval = input("Enter the data interval (e.g., 1m, 5m, 1wk): ")

    try:
        data = Data()

        # convert to pandas data types
        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        interval = pd.Timedelta(interval)

        # Get price data using the GetData class
        df = data.get_price_data(start=start_date, end=end_date, interval=interval, ticker=ticker)

        # Display the retrieved data
        print("Price data for {} from {} to {}:".format(ticker, start_date, end_date))
        print(df)
    except Exception as e:
        print("An error occurred:", str(e))

main()