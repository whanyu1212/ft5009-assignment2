import pandas as pd
import numpy as np


class IndexBuilder:
    def __init__(
        self, input_data: pd.DataFrame, shares_outstanding_data: pd.DataFrame = None
    ):
        self.data = input_data.copy()
        if shares_outstanding_data is not None:
            self.shares_outstanding_data = shares_outstanding_data.copy()

    def build_equal_weighted_index(self, base_value: float = 1.0) -> pd.DataFrame:
        """Builds an equal-weighted index from the input OHLCV data.

        Returns:
            pd.DataFrame: A DataFrame containing the equal-weighted index values.
        """

        # Note: We took care of the following steps in the DataProcessor
        # Just to be safe, we do it again here.
        if "Return" not in self.data.columns:
            raise ValueError(
                "Input data must contain 'Return' column. "
                "Please run DataProcessor first."
            )
        index_df = (
            self.data.groupby("Date")["Return"]
            .mean()
            .add(1)  # Convert returns to growth factor
            .cumprod()  # Cumulative product to get index value
            .mul(base_value)  # Scale to base value. E.g., start at 1.0
            .reset_index()
            .rename(columns={"Return": "Equal_Weighted_Index"})
        )

        return index_df

    def build_price_weighted_index(self) -> pd.DataFrame:
        """Builds a price-weighted index from the input OHLCV data.

        Returns:
            pd.DataFrame: A DataFrame containing the price-weighted index values.
        """

        if "Close_normalized" not in self.data.columns:
            raise ValueError(
                "Input data must contain 'Close_normalized' column. "
                "Please run DataProcessor first."
            )

        # Calculate the price-weighted index
        index_df = (
            self.data.groupby("Date")["Close_normalized"]
            .sum()  # Total closing price across all symbols
            .div(self.data["Symbol"].nunique())  # Normalize to first date's average
            .reset_index()
            .rename(columns={"Close_normalized": "Price_Weighted_Index"})
        )

        return index_df

    def build_value_weighted_index(self, base_value: float = 1.0) -> pd.DataFrame:
        """Builds a value-weighted index from the input OHLCV data.

        Args:
            base_value (float, optional): Base value for the index. Defaults to 1.0.

        Raises:
            ValueError: If shares outstanding data is not provided.

        Returns:
            pd.DataFrame: A DataFrame containing the value-weighted index values.
        """

        if self.shares_outstanding_data is None:
            raise ValueError(
                "Shares outstanding data must be provided for value-weighted index."
            )

        merged_df = pd.merge(
            self.data, self.shares_outstanding_data, on="Symbol", how="left"
        )

        # Calculate daily market cap
        merged_df["Daily_Market_Cap"] = (
            merged_df["Close"] * merged_df["sharesOutstanding"]
        )

        total_market_cap = merged_df.groupby("Date")["Daily_Market_Cap"].sum()

        merged_df["Weight"] = merged_df.apply(
            lambda row: row["Daily_Market_Cap"] / total_market_cap[row["Date"]],
            axis=1,
        )

        merged_df["Weighted_Return"] = merged_df["Return"] * merged_df["Weight"]

        index_df = (
            merged_df.groupby("Date")["Weighted_Return"]
            .sum()
            .add(1)
            .cumprod()
            .mul(base_value)
            .reset_index()
            .rename(columns={"Weighted_Return": "Value_Weighted_Index"})
        )

        return index_df

    def build_risk_parity_index(
        self, base_value: float = 1.0, rolling_window: int = 252
    ) -> pd.DataFrame:
        """Builds a risk parity-based index from the input OHLCV data.

        Args:
            base_value (float, optional): Base value for the index. Defaults to 1.0.
            rolling_window (int, optional): Rolling window size for volatility calculation. Defaults to 252.

        Returns:
            pd.DataFrame: A DataFrame containing the risk parity-based index values.
        """

        # pivot first so easier to work with for calculating volatility
        returns_df = self.data.pivot(index="Date", columns="Symbol", values="Return")

        volatility = (
            returns_df.rolling(window=rolling_window, min_periods=1).std().fillna(0)
        )

        inverse_volatility = 1 / volatility

        inverse_volatility.replace([np.inf, -np.inf], np.nan, inplace=True)
        inverse_volatility.fillna(0, inplace=True)

        sum_inverse_volatility = inverse_volatility.sum(axis=1)

        weights = inverse_volatility.div(sum_inverse_volatility, axis=0)
        weights.fillna(0, inplace=True)

        weighted_returns = (returns_df * weights).sum(axis=1)

        index_df = (
            weighted_returns.add(1)
            .cumprod()
            .mul(base_value)
            .reset_index()
            .rename(columns={0: "Risk_Parity_Index"})
        )

        return index_df

    def build_index(
        self, type: str, base_value: float = 1.0, rolling_window: int = 252
    ) -> pd.DataFrame:
        """Builds both equal-weighted and price-weighted indexes.

        Args:
            type (str): Type of index to build. Options are "equal", "price", "value", or "risk_parity".
            base_value (float, optional): Base value for the equal weighted index.
            Defaults to 1.0.

        Raises:
            ValueError: If the index type is invalid.

        Returns:
            pd.DataFrame: A DataFrame containing the requested index values.
        """
        if type == "equal":
            return self.build_equal_weighted_index(base_value=base_value)
        elif type == "price":
            return self.build_price_weighted_index()
        elif type == "value":
            return self.build_value_weighted_index(base_value=base_value)
        elif type == "risk_parity":
            return self.build_risk_parity_index(
                base_value=base_value, rolling_window=rolling_window
            )
        else:
            raise ValueError(
                "Invalid index type. Choose 'equal', 'price', 'value', or 'risk_parity'."
            )
