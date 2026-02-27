from typing import Optional

import pandas as pd
import numpy as np

from Asset import Asset
from InputHandler import InputHandler


class Portfolio:
    def __init__(self, assets: dict, weights: Optional[dict] = None):
        self.assets = assets
        if weights is None:
            equal_weight = 1 / len(assets.keys())
            self.weights = {key: equal_weight for key in assets.keys()}
        else:
            self.weights = weights
        self.weight_rfa = 1 - sum(self.weights.values())

        self.assets_return_df = None
        self.calculate_assets_returns()

        self.correlation_matrix = np.eye(len(self.assets.keys()))
        self.covariance_matrix = np.eye(len(self.assets.keys()))
        self.calculate_covariance_and_correlation_matrix()

        self.portfolio_mean_return = None
        self.portfolio_stdev = None

    def add_asset_to_portfolio(self, new_asset_name: str, new_asset: Asset) -> None:
        self.assets[new_asset_name] = new_asset

    def remove_asset_from_portfolio(self, asset_name: str):
        del self.assets[asset_name]

    def update_weight_rfa(self):
        self.weight_rfa = 1 - sum(self.weights.values())

    def calculate_assets_returns(self):
        # 1) create a dataframe with all time series
        all_prices = pd.concat([single_asset.price_time_series_df for name, single_asset in self.assets.items()],
                               join='outer', axis=1)
        # 2) check the dataframe
        num_days_raw = len(all_prices)
        reduced_prices_df = all_prices.dropna(how='any', axis=0)
        if len(reduced_prices_df) < num_days_raw:
            print('%s rows with missing price data' % (len(reduced_prices_df) - num_days_raw))
            # 3) clean dataframe
            all_prices = InputHandler.fill_missing_values_in_price_time_series(all_prices)
            print('price time series cleaned')

        # 4) calculate returns
        returns = (all_prices - all_prices.shift(1)) / all_prices.shift(1)
        returns = returns.dropna()
        self.assets_return_df = returns

    def calculate_covariance_and_correlation_matrix(self):
        # calculate correlation matrix
        self.covariance_matrix = self.assets_return_df.cov(ddof=1)
        self.correlation_matrix = self.assets_return_df.corr(method='pearson')

    def get_correlation_matrix(self):
        return self.correlation_matrix

    def get_covariance_matrix(self):
        return self.covariance_matrix
