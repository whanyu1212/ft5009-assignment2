import enum
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Optional, List

import statsmodels.api as sm


@dataclass
class AssignmentConfig:
    trading_days: int = 252
    stock_list: List[str] = None

    def __post_init__(self):
        if self.stock_list is None:
            self.stock_list = ["VTRS", "AAPL", "GOOG", "META", "WMT"]
            self.benchmark_index = "^GSPC"
