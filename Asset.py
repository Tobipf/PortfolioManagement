class Asset:
    def __init__(self, ticker, asset_class, price_time_series_df):
        self.ticker = ticker
        self.asset_class = asset_class
        self.price_time_series_df = price_time_series_df
        self.return_time_series_df = None
        self.return_mean = None
        self.return_stdev = None

        self.calculate_return_time_series()
        self.calculate_mean_return()
        self.calculate_return_stdev()

    def set_price_time_series(self, time_series_df):
        self.price_time_series_df = time_series_df

    def get_price_time_series(self):
        return self.price_time_series_df

    def calculate_return_time_series(self, days: int = 1) -> None:
        self.return_time_series_df = self.price_time_series_df - self.price_time_series_df.shift(days)

    def get_return_time_series(self):
        return self.return_time_series_df

    def calculate_mean_return(self) -> None:
        self.return_mean = self.return_time_series_df.mean()

    def get_mean_return(self) -> float:
        return self.return_mean

    def calculate_return_stdev(self) -> None:
        self.return_stdev = self.return_time_series_df.std()

    def get_return_stdev(self) -> float:
        return self.return_stdev
