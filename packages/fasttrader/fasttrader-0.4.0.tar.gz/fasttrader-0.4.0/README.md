# Backtester
This project allows you to backtest your trading strategies with historical stock market data. 

## Getting started

Get a copy of the project locally
> git clone https://github.com/CS594GROUP2/backtester

Automate virtual environment creation and dependency installation by executing `setup.sh` inside the project folder:
> ./setup.sh

Note: bash shell scripting is not supported natively on windows but you can use wsl/wsl2 to run it.

### Activate the virtual environment (CL)

Now, switch to the newly created virtual environment by running:
> source env/bin/activate

To test for successful setup:
> pip list

You should see a number of dependencies installed including pandas and yfianance.

## Project Structure

### Core folder
This folder should contain all of files and methods we will implement for our project. This way should there a need to intergrate more features such as testing or web front-end, it will be easier to manage. 


### Testing
The project utilizes Pytest framework for testing. To test run the following command in the root folder:
> pytest

for more detail

> pytest -vv