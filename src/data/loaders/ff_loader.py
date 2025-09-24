import pandas_datareader.data as web
import pandas as pd


class FamaFrenchLoader:
    def __init__(self, start: str = "2015-01-01", end: str = "2024-12-31"):
        self.start = start
        self.end = end

    def _get_fama_french_data(self, series_name: str) -> pd.DataFrame:
        """Fetches data from the Fama-French library for a given series.

        Args:
            series_name (str): The name of the data series to fetch.

        Returns:
            pd.DataFrame: A DataFrame containing the requested Fama-French data.
        """
        data = web.DataReader(
            series_name, "famafrench", start=self.start, end=self.end
        )[0]
        # data.index = pd.to_datetime(data.index, format="%Y%m")
        return data

    def get_fama_french_factors(self) -> pd.DataFrame:
        """Fetches the Fama-French 3-Factor data.

        Returns:
            pd.DataFrame: A DataFrame containing the Fama-French factors.
        """
        ff_factors = self._get_fama_french_data("F-F_Research_Data_Factors_daily")
        ff_factors.columns = ["Mkt-RF", "SMB", "HML", "RF"]
        return ff_factors

    def get_momentum_factor(self) -> pd.DataFrame:
        """Fetches the Fama-French Momentum factor data.

        Returns:
            pd.DataFrame: A DataFrame containing the Momentum factor.
        """
        momentum_factor = self._get_fama_french_data("F-F_Momentum_Factor_daily")
        momentum_factor.columns = ["MOM"]
        return momentum_factor

    def get_ff_momentum_factor(self) -> pd.DataFrame:
        """Fetches and merges the Fama-French 3-Factor data with the Momentum factor.

        Returns:
            pd.DataFrame: A DataFrame containing the merged Fama-French and Momentum factors.
        """
        ff_factors = self.get_fama_french_factors()
        momentum_factor = self.get_momentum_factor()
        ff_momentum_factor = pd.merge(
            ff_factors, momentum_factor, left_index=True, right_index=True, how="inner"
        ).reset_index()
        return ff_momentum_factor


if __name__ == "__main__":
    # Example usage:
    loader = FamaFrenchLoader(start="2020-01-01", end="2023-12-31")
    ff_momentum_data = loader.get_ff_momentum_factor()
    print("Fama-French 3-Factor + Momentum Data:")
    print(ff_momentum_data.head())

    ff_data = loader.get_fama_french_factors()
    print("\nFama-French 3-Factor Data:")
    print(ff_data.head())

    momentum_data = loader.get_momentum_factor()
    print("\nMomentum Factor Data:")
    print(momentum_data.head())
