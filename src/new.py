class Analysis:
  def __init__(self, ticker, start_date):
    self.ticker = ticker.lower()
    self.start_date = start_date
    self.df = get_stock_data(self.ticker, start_date=self.start_date)
    print(self.df.head())

    # -- CONFIG -- #
    self.comp_stocks = ['xlk', 'spy', 'twlo']
    self.grow_amount = 100

  def chart(self):
    self.time_series()
    self.k_growth()
    self.est_sales_v_px()
    self.p_sup_v_p_px()

  def time_series(self):
    # Basic time series
    go.Figure(data=[go.Candlestick(
        x=self.df.index,
        open=self.df['Open'],
        high=self.df['High'],
        low=self.df['Low'],
        close=self.df['Close'])]).show()

  def k_growth(self):
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
      normalized = ks[i] * dfs[i]['Close']
      sns.lineplot(
          self.df.index,
          normalized,
          ax=ax, color=colors[i], label=self.comp_stocks[i],
      )
      '''
      print(self.comp_stocks[i])
      print(normalized)
      print()
      print()

      print(self.ticker)
      print(main_k * self.df['Close'])
      '''
    ax.legend()

  # Estimated sales versus stock price daily
  def est_sales_v_px(self):
    # Data prep & cleaning
    df = pd.read_csv(f'/content/{self.ticker}_daily_est.csv')
    print(df.head())

    # Calc day over day change
    daily_est = df['est_sales'].pct_change(1)
    daily_px = df['px'].pct_change(1)

    print(df.head())

    # Plot px and rev on the same time series
    fig, ax1 = plt.subplots(figsize=(20, 10))
    ax1.set_xlabel('time')
    ax1.set_ylabel('px')
    ax1 = sns.lineplot(df.index, df['px'])
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.set_ylabel('expected revenue')
    ax2.tick_params(axis='y')
    ax2 = sns.lineplot(df.index, df['est_sales'], color='red')

  # % surprise vs stock % change quarterly
  def p_sup_v_p_px(self):
    # df = pd.read_csv(f'/content/{self.ticker}_sup.csv')
    pass

ddog = Analysis('ddog', start_date='2019-09-20')
ddog.chart()

twlo = Analysis('twlo', start_date='2016-06-24')
twlo.chart()
