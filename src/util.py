from dataclasses import dataclass, field
from typing import List


@dataclass
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
