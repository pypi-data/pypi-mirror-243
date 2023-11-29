import matplotlib.pyplot as plt
import pandas as pd


class Visualizer:

    def __init__(self) -> None:
        pass

    def visualize_strategy(self, price_data, trading_signals, win_loss_percents, portfolio_values, column_index='Close'):
        self.generate_line_plot(price_data, portfolio_values, trading_signals, column_index)
        self.generate_bubble_plot(price_data, win_loss_percents)

    def generate_line_plot(self, price_data: pd.Series, portfolio_values, trading_signals, column_index='Close'):

        """
            Displays a line plot that represents the results of a given trading strategy, with lines to represent
            the price data for the asset, portfolio values, and trading signal indicators. Note that portfolio values
            are normalized relative to the price data
            Args:
                price_data: A Pandas DataFrame containing the price data in OHLCV format
                portfolio_values: A NumPy array containing the portfolio values to be plotted
                trading_signals: A NumPy array containing buy and sell indicators
                column_index: Index for which column in the price_data will be plotted, defaults to 'Close'
        """

        if len(price_data) != len(portfolio_values):
            raise ValueError('price_data must be the same length as portfolio_values')
        if len(portfolio_values) != len(trading_signals):
            raise ValueError('portfolio_values must be the same length as trading_signals')

        try:
            price_data_column = price_data[column_index]
        except KeyError:
            print(f"{column_index} is not a valid index for price_data")


        # graph the price_data values:
        stock_line = plt.plot(price_data[column_index], label='Asset Price', color='blue', linewidth=1)

        # graph normalized portfolio values to compare to price_data:
        normalized_portfolio_values = (portfolio_values / portfolio_values[0]) * price_data_column[0]
        plt.plot(price_data.index, normalized_portfolio_values, label='Normalized Portfolio Value', color='green')

        # create a list of dates to match the positive and negative trading signals:
        buy_dates = []
        sell_dates = []

        for i in range(len(trading_signals)):
            if trading_signals[i] > 0:
                buy_dates.append(price_data.index[i])
            elif trading_signals[i] < 0:
                sell_dates.append(price_data.index[i])

        # plot the trading signals using scatter function:

        plt.scatter(buy_dates, price_data_column[trading_signals > 0],
                    label='Buy', color='green', marker='^', linewidths=3)

        plt.scatter(sell_dates, price_data_column[trading_signals < 0],
                    label='Sell', color='red', marker='v', linewidths=3)

        # set labels and display the graph:
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Strategy Result')
        plt.legend(loc='best')

        plt.show()

    def generate_bubble_plot(self, price_data: pd.Series, win_loss_percents):
        """
                Displays a bubble plot that represents the results of a given trading strategy, with bubbles to 
                represent the success of each trade made by the strategy. 
                Args:
                    price_data: A Pandas DataFrame containing the price data in OHLCV format
                    win_loss_percents: A NumPy array containing the win/loss percentages for the strategy
        """
        
        # Separate winning and losing trades
        winning_trades = [perc > 0 for perc in win_loss_percents]
        losing_trades = [perc < 0 for perc in win_loss_percents]

        print("Total Trades:", len(win_loss_percents))
        print("Winning Trades:", sum(winning_trades))
        print("Losing Trades:", sum(losing_trades))

        # Array of winning values
        winning_values = [round(perc, 4) for perc, win in zip(win_loss_percents, winning_trades) if win]

        print("Winning Bubble Sizes:", winning_values)

        # Array of losing values
        losing_values = [round(perc, 4) for perc, lose in zip(win_loss_percents, losing_trades) if lose]

        print("Losing Bubble Sizes:", losing_values)

        # Create a scatter plot with green bubbles for winning trades and red for losing trades
        plt.figure(figsize=(12, 6))
        plt.scatter(
            price_data.index,  # Use timestamps for the X-axis
            win_loss_percents,
            s=[abs(value) * 20000 for value in win_loss_percents],
            c=['g' if win else 'r' for win in winning_trades],  # Use green for winning trades and red for losing trades
            edgecolor='black'
        )

        plt.xlabel("Time Frame")
        plt.ylabel("Profit/Loss")
        plt.title("Bubble Plot of Winning and Losing Trade Profit/Loss")

        # Format the X-axis to display dates as labels
        plt.xticks(rotation=45)

        # Adjust plot size to fit the screen
        plt.tight_layout()

        # Show the plot
        plt.show()