import pandas as pd
from typing import Literal, Callable


class DataProcessor:
    def __init__(
        self,
        input_olhcv_data: pd.DataFrame,
        normalize_method: Literal["rebasing", "minmax", "zscore"] = "rebasing",
    ):
        self.data = input_olhcv_data.copy()
        self.normalize_method = normalize_method

    def process_data(self) -> pd.DataFrame:
        """Main processing pipeline that applies all transformations.

        Raises:
            ValueError: If the normalization method is unknown.

        Returns:
            pd.DataFrame: Processed data with additional columns.
        """
        # Define the mapping from method name to normalization function
        normalization_functions: dict[str, Callable[[pd.Series], pd.Series]] = {
            "rebasing": self._rebasing_normalization,
            "minmax": self._minmax_normalization,
            "zscore": self._zscore_normalization,
        }

        if self.normalize_method not in normalization_functions:
            raise ValueError(
                f"Unknown normalization method: {self.normalize_method}. "
                f"Available methods: {list(normalization_functions.keys())}"
            )

        # Prepare and process data using method chaining
        processed_data = (
            self.data.assign(Date=pd.to_datetime(self.data["Date"]))
            .sort_values(by=["Symbol", "Date"])
            .reset_index(drop=True)
            .assign(
                Return=lambda df: df.groupby("Symbol")["Close"].pct_change(),
                Close_normalized=lambda df: df.groupby("Symbol")["Close"].transform(
                    normalization_functions[self.normalize_method]
                ),
            )
        )
        return processed_data

    @staticmethod
    def _rebasing_normalization(x: pd.Series) -> pd.Series:
        """Normalize prices relative to the first value (rebasing to 1.0).

        Args:
            x (pd.Series): Input price series.

        Returns:
            pd.Series: Normalized price series.
        """
        return x / x.iloc[0]

    @staticmethod
    def _minmax_normalization(x: pd.Series) -> pd.Series:
        """Normalize prices using min-max scaling (0-1 range).

        Args:
            x (pd.Series): Input price series.

        Returns:
            pd.Series: Normalized price series.
        """
        return (x - x.min()) / (x.max() - x.min())

    @staticmethod
    def _zscore_normalization(x: pd.Series) -> pd.Series:
        """Normalize prices using z-score standardization.

        Args:
            x (pd.Series): Input price series.

        Returns:
            pd.Series: Normalized price series.
        """
        return (x - x.mean()) / x.std()
