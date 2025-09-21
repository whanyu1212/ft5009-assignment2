import os
import csv
import requests
import pandas as pd
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import time
from loguru import logger

load_dotenv()


class AlphaVantageLoader:
    """Loader for fetching financial data from Alpha Vantage API."""

    def __init__(
        self,
        api_key: str = None,
        max_retries: int = 5,
        delay: float = 3.0,
    ):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("Alpha Vantage API key must be provided")
        self.max_retries = max_retries
        self.delay = delay

    # === Public Methods ===
    def get_listing_status(self) -> pd.DataFrame:
        """Fetches the current listing status of all securities.
        This API end point returns a csv file and thus we will
        not be reusing the private _make_api_request method.
        All the symbols are US listed securities.

        Returns:
            pd.DataFrame: The listing status of all securities.
        """

        CSV_URL = f"https://www.alphavantage.co/query?function=LISTING_STATUS&date=2015-01-01&state=active&apikey={self.api_key}"

        with requests.Session() as s:
            download = s.get(CSV_URL)
            decoded_content = download.content.decode("utf-8")
            cr = csv.reader(decoded_content.splitlines(), delimiter=",")
            my_list = list(cr)
            df = pd.DataFrame(my_list[1:], columns=my_list[0])
            print(df.head())
            # Filter to include only active stocks
            df = df.loc[
                (df["assetType"] == "Stock") & (df["status"] == "Active")
            ].reset_index(drop=True)
            return df


if __name__ == "__main__":
    loader = AlphaVantageLoader()
    df = loader.get_listing_status()
    df.to_parquet("./data/listing_status.parquet", index=False)
