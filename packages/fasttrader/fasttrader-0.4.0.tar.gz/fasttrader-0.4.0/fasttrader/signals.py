import numpy as np
import pandas as pd
import numba as nb 

# HELPER FUNCTIONS
@nb.jit(nopython=True)
def generate_random(size, entp, extp):
    random_signals = np.zeros(shape=size, dtype=np.int8)
    random_values = np.random.random(size)
    in_position = False

    # iterate through array, going in and out of position based on the random values
    for i in range(random_signals.size):
        if in_position:
            if extp > random_values[i]:
                random_signals[i] = -1
                in_position = False
        else:
            if entp > random_values[i]:
                random_signals[i] = 1
                in_position = True
    
    return random_signals

@nb.jit(nopython=True)
def generate_signals(price_data_np, target_np):
    signals = np.zeros_like(price_data_np, dtype=np.int8)
    in_position = False

    # iterate through grabbing items from prifce_data_np and target_np
    for i in range(1, price_data_np.size):
        if target_np[i] == 0:
            pass
        if price_data_np[i] > target_np[i] and not in_position:
            signals[i] = 1
            in_position = True
        elif price_data_np[i] < target_np[i] and in_position:
            signals[i] = -1
            in_position = False
        else:
            pass
    
    return signals

class SignalGenerator:

    def __init__(self, price_data, metadata={}):
        self.price_data : pd.Series = price_data
        self.metadata : dict = metadata
        self.trading_signals : np.ndarray = None

    def generate_crossover(self, crossover_data1, crossover_data2, metadata={}) -> np.ndarray:
        """
        Generates trading signals and stores them in a newly generated numpy array
        
        Args:
        crossover_data1: a Pandas Series containing the crossover data
        crossover_data2: a Pandas Series containing the crossover data
        metadata: a Dict containing the metadata for the price data, included in get_results()
        
        Returns:
        a NumPy array of trading signals
        """
        if not isinstance(crossover_data1, pd.Series) or not isinstance(crossover_data2, pd.Series):
            raise ValueError("The crossover data is not a Pandas Series")
        
        # update the metadata
        for key, value in metadata.items():
            self.metadata[key] = value
        
        # numba only works with numpy arrays
        cross1_np = crossover_data1.to_numpy()
        cross2_np = crossover_data2.to_numpy()

        self.trading_signals = generate_signals(cross1_np, cross2_np)

        return self.trading_signals


    def generate_random(self, size, entry_probability, exit_probability) -> np.ndarray:
        """
            Returns random trading strategy for a given size, entry and exit probability.

            Args:
            size: The size of the dataset.
            entry_probability: Float from 0 to 1 that indicates the chance that the random strategy will enter a position.
            exit_probability: Float from 0 to 1 that indicates the chance that the random strategy will leave a position.
            Returns:
            An array of trading signals that reflect a random trading strategy.
        """

        # Exceptions:
        if size <= 0:
            raise ValueError("Size must be greater than 0")
        if entry_probability < 0 or entry_probability > 1:
            raise ValueError("entry_probability must be between 0 and 1")
        if exit_probability < 0 or exit_probability > 1:
            raise ValueError("exit_probability must be between 0 and 1")
        
        # update the metadata
        self.metadata = {
            "random_signals": True
        }

        self.trading_signals = generate_random(size, entry_probability, exit_probability)

        return self.trading_signals

    def generate_above_below(self, target, metadata={}) -> np.ndarray:
        """
        Generates trading signals and stores them in a newly generated numpy array
        a positive trading signal(+1) is generated when the price crosses above the target
        a negative trading signal(-1) is generated when the price crosses below the target
        it is assumed to start not already in a position
        

        Args:
        target: a Pandas Series containing the target data crossover values
        metadata: a Dict containing the metadata for the price data, included in get_results()
        
        Returns:
        a NumPy array of trading signals
        """

        # validate the price data (defensive programming)
        if not isinstance(self.price_data, pd.Series):
            raise ValueError("The price data is not a Pandas Series")
        
        # validate the target data
        if not isinstance(target, pd.Series):
            raise ValueError("The target data is not a Pandas Series")
        
        # update the metadata
        self.metadata = metadata

        # numba only works with numpy arrays
        price_data_np = self.price_data.to_numpy()
        target_np = target.to_numpy()
        
        self.trading_signals = generate_signals(price_data_np, target_np)

        return self.trading_signals

    def get_results(self) -> dict:
        """
        Returns:
        A list containing:
        a Numpy array of trading signals
        a Numpy array of the price data
        a List of metadata
        """

        results = {
            "trading_signals": self.trading_signals,
            "price_data": self.price_data,
            "metadata": self.metadata
        }

        return results