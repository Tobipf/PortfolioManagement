import pandas as pd
from pathlib import Path
import datetime
import yfinance
from fredapi import Fred
from typing import Union


class InputHandler:
    def __init__(self, passwords_filepath: Union[Path, str]):
        self.passwords_filepath = passwords_filepath
        self.fred_object = Fred(self._get_fred_api_key())

    def _get_fred_api_key(self) -> str:
        _pw_file = pd.read_json(self.passwords_filepath, typ="series")
        _fred_api_key = _pw_file['fred_api_key']
        return _fred_api_key

    @staticmethod
    def _download_time_series_data_from_yfinance(ticker: list,
                                                 start_date: Union[str, datetime.date] = '2007-01-01',
                                                 end_date: Union[str, datetime.date] = '2009-12-31'):
        # download data from yahoo finance
        ticker = ' '.join(ticker)
        data_yahoo = yfinance.download(tickers=ticker,  # "GOOG AMZN MSFT TEAM NVDA BIDU JD ETH-USD NSRGY NZDAUD=X",
                                       start=start_date, end=end_date, interval="1d",
                                       # group by ticker
                                       group_by='ticker',
                                       # adjust all OHLC automatically
                                       auto_adjust=True)
        return data_yahoo

    def _download_time_series_data_from_fred(self, ticker, start_date, end_date):
        # e.g. fred.get_series('DGS10', observation_start='1/1/2010', observation_end='31/12/2020')
        return self.fred_object.get_series(ticker, observation_start=start_date, observation_end=end_date)

    def read_time_series_data_from_database(self):
        pass  # TODO

    def save_time_series_data_to_database(self):
        pass  # TODO

    def get_closing_prices(self, ticker: list, start_date: Union[str, datetime.date],
                           end_date: Union[str, datetime.date]) -> pd.DataFrame:
        """
        This function downloads time series data from Yahoo finance. It filters the result for closing prices and
        returns a dataframe of these closing prices for all tickers in the range from start_date to end_date.

        :param ticker: list, list of tickers to download the closing prices for.
        :param start_date: start date of the price time series
        :param end_date: end date of the price time series
        :return:
        """
        # TODO: check whether data in database
        data_df = self._download_time_series_data_from_yfinance(ticker, start_date, end_date)
        entries = data_df.columns.to_list()
        assets = list(set([entry[0] for entry in entries]))
        data_close_df = pd.DataFrame()
        for asset in assets:
            data_close_df[asset] = data_df[asset, 'Close']
        return data_close_df

    @staticmethod
    def fill_missing_values_in_price_time_series(price_time_series_df: pd.DataFrame) -> pd.DataFrame:
        price_time_series_df.ffill(axis=0, inplace=True, limit=5)
        price_time_series_df.bfill(axis=0, inplace=True, limit=5)
        price_time_series_df = price_time_series_df.interpolate(method='time')
        return price_time_series_df

