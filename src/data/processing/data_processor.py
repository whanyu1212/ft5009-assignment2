import pandas as pd


class DataProcessor:
    def __init__(self, input_olhcv_data: pd.DataFrame):
        self.data = input_olhcv_data.copy()
        self.normalize_method = normalize_method

    def _calculate_returns(self):
        pass

    def _get_normalized_daily_price(self, normalize_method="rebasing"):
        pass
