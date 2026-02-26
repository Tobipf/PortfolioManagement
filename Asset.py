import pandas as pd


class Asset:
    def __init__(self, ticker: str, asset_class: str, price_time_series_df: pd.DataFrame):
        self.ticker = ticker
        self.asset_class = asset_class
        self.price_time_series_df = price_time_series_df
        self.return_time_series_df = None
        self.return_mean = None
        self.return_stdev = None

        self.calculate_return_time_series()
        self.calculate_mean_return()
        self.calculate_return_stdev()

    def set_price_time_series(self, time_series_df: pd.DataFrame) -> None:
        self.price_time_series_df = time_series_df

    def get_price_time_series(self) -> pd.DataFrame:
        return self.price_time_series_df

    def calculate_return_time_series(self, days: int = 1) -> None:
        _shifted_returns = self.price_time_series_df.shift(days)
        self.return_time_series_df = (self.price_time_series_df - _shifted_returns) / _shifted_returns

    def get_return_time_series(self) -> pd.DataFrame:
        return self.return_time_series_df

    def calculate_mean_return(self) -> None:
        self.return_mean = self.return_time_series_df.mean()

    def get_mean_return(self) -> float:
        return self.return_mean

    def calculate_return_stdev(self) -> None:
        self.return_stdev = self.return_time_series_df.std()

    def get_return_stdev(self) -> float:
        return self.return_stdev
