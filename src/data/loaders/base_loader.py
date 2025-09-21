from abc import ABC, abstractmethod
import pandas as pd
from typing import List, Union, Optional, Any


class BaseLoader(ABC):
    """Abstract base class for data loaders."""

    @abstractmethod
    def get_daily_ohlcv(
        self,
        tickers: Union[List[str], str],
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:

        raise NotImplementedError

    # @abstractmethod
    # def get_stock_info(
    #     self,
    #     tickers: Union[List[str], str],
    #     fields: Union[List[str], None] = None,
    #     as_dataframe: bool = True,
    # ) -> Union[pd.DataFrame, List[dict]]:

    #     raise NotImplementedError
