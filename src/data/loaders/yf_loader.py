import yfinance as yf
import pandas as pd
import time
from loguru import logger
from typing import List, Union, Optional, Any


class YFinanceLoader:
    def __init__(self, max_retries: int = 3, delay: float = 1.0):
        self.max_retries = max_retries
        self.delay = delay

    def get_daily_ohlcv(
        self,
        tickers: Union[List[str], str],
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> pd.DataFrame:
        """Fetch daily OHLCV data for given tickers.

        Args:
            tickers (Union[List[str], str]): The stock ticker symbols to fetch data for.
            start (Optional[str], optional): The start date for the data in 'YYYY-MM-DD' format. Defaults to None.
            end (Optional[str], optional): The end date for the data in 'YYYY-MM-DD' format. Defaults to None.
        Returns:
            pd.DataFrame: A DataFrame containing the OHLCV data.
        """
        if isinstance(tickers, str):
            tickers = [tickers]

        all_data = []
        for ticker in tickers:
            for attempt in range(self.max_retries):
                try:
                    df = yf.download(ticker, start=start, end=end)
                    df.columns = df.columns.droplevel(1)
                    df = df.reset_index().rename_axis(None, axis=1)
                    df["Symbol"] = ticker
                    all_data.append(df)

                except Exception as e:
                    logger.error(
                        f"Error fetching data for {ticker} (attempt {attempt + 1}/{self.max_retries}): {e}"
                    )
                    if attempt < self.max_retries - 1:
                        time.sleep(self.delay)
                    else:
                        logger.error(
                            f"Failed to fetch data for {ticker} after {self.max_retries} attempts."
                        )
                else:
                    break
        df_final = pd.concat(all_data, axis=0)
        df_final["Date"] = pd.to_datetime(df_final["Date"])

        return df_final

    def get_stock_info(
        self,
        tickers: Union[List[str], str],
        fields: Union[List[str], None] = None,
        as_dataframe: bool = True,
    ) -> Union[pd.DataFrame, List[dict]]:
        """Fetch stock information from Yahoo Finance.

        Args:
            tickers (Union[List[str], str]): The stock ticker symbols to fetch data for.
            fields (Union[List[str], None], optional): The specific fields to retrieve. Defaults to None.
            as_dataframe (bool, optional): Whether to return the data as a DataFrame. Defaults to True.

        Returns:
            Union[pd.DataFrame, List[dict]]: The stock information, either as a DataFrame or a list of dictionaries.
        """

        if isinstance(tickers, str):
            tickers = [tickers]

        stock_data = []
        for ticker in tickers:
            for attempt in range(self.max_retries):
                try:
                    data = yf.Ticker(ticker).info

                    if fields:
                        filtered_data = {
                            field: data.get(field, None) for field in fields
                        }
                        # keep the symbol so we can group by it later
                        filtered_data["symbol"] = ticker
                        stock_data.append(filtered_data)
                    else:
                        stock_data.append(data)
                    break  # Success, exit retry loop
                except Exception as e:
                    logger.error(
                        f"Error fetching data for {ticker} (attempt {attempt + 1}/{self.max_retries}): {e}"
                    )
                    if attempt < self.max_retries - 1:
                        time.sleep(self.delay)
                    else:
                        logger.error(
                            f"Failed to fetch data for {ticker} after {self.max_retries} attempts."
                        )

        if as_dataframe:
            return pd.DataFrame(stock_data)
        return stock_data
