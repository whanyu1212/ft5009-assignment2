from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)  # Read-only, immutable after creation
class AssignmentConfig:
    """
    Configuration class for the assignment.
    """

    trading_days: int = 252
    stock_list: List[str] = field(
        default_factory=lambda: ["AAPL", "MSFT", "GOOGL", "XOM", "INTC"]
    )
    benchmark_index: str = "^GSPC"
    risk_free_rate: float = 0.04
    daily_adjusted_risk_free_rate: float = (1 + risk_free_rate) ** (
        1 / trading_days
    ) - 1
    start_date: str = "2015-01-01"
    end_date: str = "2024-12-31"
