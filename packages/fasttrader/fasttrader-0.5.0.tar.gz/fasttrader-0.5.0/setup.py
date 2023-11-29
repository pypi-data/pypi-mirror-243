from setuptools import setup, find_packages

long_description = """
# FastTrader: Empowering Financial Analysis

FastTrader is a pioneering tool designed to empower users in the dynamic world of quantitative financial analysis. At its core, FastTrader is built on a commitment to transparency and user-driven functionality. Unlike many other platforms, we provide complete visibility into the inner workings of our system, enabling you not only to utilize but also to comprehend every facet of your trading strategies.

## Democratizing Financial Decision-Making

What truly sets FastTrader apart is our dedication to democratizing financial decision-making. Our open-source approach ensures that everyone, from individual investors to professional analysts, has equal access to sophisticated tools. We foster a community where knowledge and resources are openly shared, creating an environment where financial analysis becomes accessible to all.

## Unmatched Speed

Speed is paramount in financial analysis, and FastTrader excels in this regard. Leveraging the power of Numba, an advanced performance compiler, FastTrader accelerates numerous functions. This technological edge allows you to test potentially thousands of trading strategies in real-time, providing you with a significant advantage in today's fast-paced market.

## Join Us on the Journey

Join us on this journey to reshape financial analysis. With FastTrader, your strategies are limited only by your imagination.

## Disclaimer

**Disclaimer:** None of the research derived from this software constitutes financial advice. The contributors of this software shall not be held liable for its accuracy or the outcome of any decisions derived from the research produced by it.
"""

# Setting up
setup(
    name='fasttrader',
    version='0.5.0',
    author='CS594GROUP2',
    author_email='<johnpiapian@gmail.com>',
    description='Welcome to FastTrader, Your Gateway to Innovative Financial Analysis!',
    url='https://github.com/CS594GROUP2/backtester',
    license='MIT',
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['yfinance', 'pandas', 'pandas_ta', 'numpy', 'numba', 'matplotlib'],
    keywords=['python', 'yfinance', 'trading', 'backtesting', 'stock market', 'trading strategies'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Financial and Insurance Industry',
        'Programming Language :: Python :: 3',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
    ]
)