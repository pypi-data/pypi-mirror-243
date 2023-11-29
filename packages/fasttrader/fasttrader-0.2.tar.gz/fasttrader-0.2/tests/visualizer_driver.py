import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd

from fasttrader.data import Data
from fasttrader.signals import SignalGenerator
from fasttrader.simulator import Simulator
from fasttrader.visualizer import Visualizer

# fetch some historical price data
data_grabber = Data()
start = pd.Timestamp('2020-01-01')
end = pd.Timestamp('2021-01-01')
interval = pd.Timedelta('1d')
ticker = 'AAPL'

price_data = data_grabber.get_price_data(start, end, interval, ticker)[0]
column_index = 'Close'

# construct a signal generator from SignalGenerator in signals.py
signal_generator = SignalGenerator(price_data[column_index])

# generate some trading signals using the random_signals method
trading_signals = signal_generator.generate_random(len(price_data), 0.08, 0.08)

# call the simulator to simulate the trading strategy
simulator = Simulator(signal_generator, 0.04)
simulator.calculate_trades_win_loss()

portfolio_values = simulator.win_loss_stats['portfolio_values']
win_loss_percents = simulator.win_loss_stats['win_loss_percents']

# generate a line plot & bubble plot using visualizer method
visualiser = Visualizer()

visualiser.visualize_strategy(price_data, trading_signals, win_loss_percents, portfolio_values, column_index)