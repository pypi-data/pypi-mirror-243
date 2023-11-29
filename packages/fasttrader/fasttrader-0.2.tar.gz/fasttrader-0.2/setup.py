from setuptools import setup, find_packages

VERSION = '0.2'
DESCRIPTION = 'Welcome to FastTrader, Your Gateway to Innovative Financial Analysis'
LONG_DESCRIPTION = 'In the dynamic world of quantitative financial analysis, FastTrader stands out as a pioneering tool designed to empower you, the user. At the heart of FastTrader is our commitment to transparency and user-driven functionality. Unlike many other platforms, we provide complete visibility into the inner workings of our system, allowing you to not just utilize but also understand every aspect of your trading strategies.'

# Setting up
setup(
    name="fasttrader",
    version=VERSION,
    author="CS594GROUP2",
    author_email="<johnpiapian@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['yfinance', 'pandas', 'pandas_ta', 'numpy', 'numba', 'matplotlib'],
    keywords=['python', 'yfinance', 'trading', 'backtesting', 'stock market', 'trading strategies'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)