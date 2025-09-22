import pandas as pd


class IndexBuilder:
    def __init__(self, input_data: pd.DataFrame):
        self.data = input_data.copy()

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

    def build_index(self, type: str, base_value: float = 1.0) -> pd.DataFrame:
        """Builds both equal-weighted and price-weighted indexes.

        Args:
            type (str): Type of index to build. Options are "equal" or "price".
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
        else:
            raise ValueError("Invalid index type. Choose 'equal' or 'price'.")
