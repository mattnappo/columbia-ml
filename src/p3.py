''' PRE CODE'''
import pandas as pd
import pandas_datareader as pdr
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

CURRENT_DATE = pd.datetime.now().date()

# Get a pandas dataframe of stock data over a certain time period
def get_stock_data(ticker,  start_date='2015-1-1', end_date=CURRENT_DATE):
  return pdr.DataReader(
      ticker.upper(),
      start=start_date,
      end=end_date,
      data_source='yahoo',
  )

def get_stocks(tickers,  start_date='2015-1-1', end_date=CURRENT_DATE):
  dfs = []
  for t in tickers:
    dfs.append(pdr.DataReader(
      t.upper(),
      start=start_date,
      end=end_date,
      data_source='yahoo',
    ))
  return dfs

''' ACTUAL CODE '''

class Analysis:
  def __init__(self, ticker, start_date):
    self.ticker = ticker
    self.start_date = start_date
    self.df = get_stock_data(self.ticker, start_date=self.start_date)
    print(self.df.head())

    # -- CONFIG -- #
    self.comp_stocks = ['xlk', 'spy']
    self.grow_amount = 1000

  def chart(self):
    self.time_series()
    self.k_chart()

  def time_series(self):
    # Basic time series
    go.Figure(data=[go.Candlestick(
        x=self.df.index,
        open=self.df['Open'],
        high=self.df['High'],
        low=self.df['Low'],
        close=self.df['Close'])]).show()

  def k_chart(self):
    # Calculate the k constants for each stock in the comp_stocks list
    main_k = self.grow_amount / self.df.loc[self.start_date, 'Close'] # The k for self.ticker
    dfs = get_stocks(self.comp_stocks, start_date=self.start_date)
    ks = []
    for i in range(len(self.comp_stocks)):
      ks.append(self.grow_amount / dfs[i].loc[self.start_date, 'Close'])

    # Chart it
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    ax.set_xlabel('time')
    ax.set_title(
        f'{self.ticker} vs {self.comp_stocks} normalized growth over time (all time)',
        fontsize=20,
    )
    ax.set_xlim([self.df.index[0], CURRENT_DATE])
    colors = ['red', 'orange', 'purple', 'green']

    sns.lineplot(
        self.df.index,
        main_k * self.df['Close'],
        ax=ax, color='blue', label=self.ticker,
    ).set_ylabel('price * k')
    for i in range(len(ks)):
      sns.lineplot(
          self.df.index,
          ks[i] * dfs[i]['Close'],
          ax=ax, color=colors[i], label=self.comp_stocks[i],
      )
    ax.legend()

ddog = Analysis('ddog', start_date='2019-09-20')
ddog.chart()
