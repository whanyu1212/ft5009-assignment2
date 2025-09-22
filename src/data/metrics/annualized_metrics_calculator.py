from dataclasses import dataclass
import numpy as np
import pandas as pd


@dataclass
class FinancialMetrics:
    """
    A dataclass to calculate key performance metrics from a series of returns.

    Can be extended to include more metrics as needed.
    """

    returns: np.ndarray
    periods_per_year: int = 252  # Default

    def __post_init__(self):
        if not isinstance(self.returns, np.ndarray):
            # Conversion to numpy array if not already
            self.returns = np.array(self.returns)

    def annualized_return(self) -> float:
        """Calculates the annualized return.

        Raises:
            ValueError: If returns array is empty.

        Returns:
            float: The annualized return.
        """
        if self.returns.size == 0:
            raise ValueError("Returns array is empty.")
        # Calculate compounded total return
        total_return = np.prod(1 + self.returns) - 1
        # Annualize the total return
        annualization_factor = self.periods_per_year / self.returns.size
        return (1 + total_return) ** annualization_factor - 1

    def annualized_volatility(self) -> float:
        """Calculates the annualized volatility (standard deviation of returns).

        Returns:
            float: The annualized volatility.
        """
        if self.returns.size < 2:
            raise ValueError("Returns array is too short.")
        return np.std(self.returns) * np.sqrt(self.periods_per_year)

    def get_all_metrics(self) -> dict:
        """Calculates both annualized financial metrics.

        Returns:
            dict: A dictionary containing all calculated metrics.
        """
        return {
            "annualized_return": self.annualized_return(),
            "annualized_volatility": self.annualized_volatility(),
        }


# Sample usage
if __name__ == "__main__":
    metrics_calculator = FinancialMetrics(returns=returns_series.values)
    metrics = metrics_calculator.get_all_metrics()
    print(metrics)
