import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import pandas_ta as pta
import matplotlib.pyplot as plt

from fasttrader.data import Data
from fasttrader.signals import SignalGenerator
from fasttrader.simulator import Simulator

# DATA
# create an instance of the Data class
data_grabber = Data()

price_data = pd.read_csv('AAPL.csv', index_col='Date', parse_dates=True)
metadata = {'start': price_data.index[0], 'end': price_data.index[-1], 'interval': '1d', 'ticker': 'AAPL', 'indicator': 'SMA', "params": {'length': 20}}
ma_20 = pta.sma(price_data['Close'], 20)
risk_free_rate = 0.04 # 4% risk free rate


# SIGNAL GENERATOR
#construct a signal generator from SignalGenerator in signals.py
strategy_instance = SignalGenerator(price_data['Close'])
# signal_generator.generate_random(100, 0.5, 0.5)
#strategy_instance.generate_above_below(ma_20, metadata)
strategy_instance.generate_crossover(ma_20, price_data['Close'], metadata)
strategy_output = strategy_instance.get_results()

# print("strategy output:\n")
# print(strategy_output)


# SIMULATOR
simulator = Simulator(strategy_instance, risk_free_rate)
simulator.simulate()
simulation_output = simulator.get_results()

print(simulation_output.keys())
print(simulator.stats)
# print(simulation_output['stats'])
# print(simulation_output['input']['price_data'])


# GRAPHING
# variables for the graph
portfolio_values_graph = simulation_output['win_loss']['portfolio_values']
price_data_graph = simulation_output['input']['price_data']
trading_signals_graph = simulation_output['input']['trading_signals']
normalized_portfolio_values = portfolio_values_graph / portfolio_values_graph[0] * price_data_graph[0]

# use matplotlib to plot the price data and the moving average overlayed on one chart
fig, ax = plt.subplots(figsize=(16,9))
ax.plot(simulation_output['input']['price_data'], label='Close')
ax.plot(ma_20, label='20 period MA')
ax.plot(price_data_graph.index, normalized_portfolio_values, label='Portfolio Values', color='green')

# create a scatter plot with the trading signals
ax.scatter(trading_signals_graph[trading_signals_graph == 1].index,
            ma_20[trading_signals_graph == 1],
            label='Buy', color='green', marker='^', linewidths=5)

# splot trading signals
ax.scatter(trading_signals_graph[trading_signals_graph == -1].index,
            ma_20[trading_signals_graph == -1],
            label='Sell', color='red', marker='v', linewidths=5)

# plot metadata
ax.legend(loc='best')
ax.set_title('Price Data w/ 20 period MA and crossover strategy signals')
ax.set_ylabel('Price')
ax.set_xlabel('Date')

plt.show()