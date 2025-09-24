import pandas as pd
import numpy as np
from scipy.optimize import minimize


class PortfolioOptimizer:
    def __init__(
        self,
        input_data: pd.DataFrame,
        risk_free_rate: float = 0.04,  # the yield on the 10-year U.S. Treasury Note, is approximately 4.14%
        iterations: int = 10000,
        seed: int = 42,
    ):
        self.data = input_data.copy()
        self.risk_free_rate = risk_free_rate
        self.iterations = iterations
        np.random.seed(seed)

        # Pivot the data to get returns for each symbol
        self.returns = self.data.pivot_table(
            index="Date", columns="Symbol", values="Return"
        )
        self.n_assets = self.returns.shape[1]
        self.mean_returns = self.returns.mean()
        self.cov_matrix = self.returns.cov() * 252

    # === Private helper methods ===#

    def _generate_random_weights_matrix(self) -> np.ndarray:
        """Generates a n x m matrix of random weights, where n is the number of iterations
        and m is the number of assets. Each row sums to 1.

        Returns:
            np.ndarray: A matrix of random weights.
        """
        weights_matrix = np.random.rand(self.iterations, self.n_assets)
        return weights_matrix / np.sum(weights_matrix, axis=1, keepdims=True)

    def _calculate_portfolio_metrics(
        self, weights_matrix: np.ndarray, return_method: str = "arithmetic"
    ) -> pd.DataFrame:
        """Calculates portfolio metrics for a matrix of weights.

        Args:
            weights_matrix (np.ndarray): a matrix of n x m weights.
            return_method (str, optional): The method to use for calculating returns.
            Defaults to "arithmetic".

        Returns:
            pd.DataFrame: A DataFrame containing the portfolio metrics.
        """
        if return_method == "arithmetic":
            port_returns = np.dot(weights_matrix, self.mean_returns) * 252
        elif return_method == "geometric":
            port_returns = (
                np.prod(1 + np.dot(weights_matrix, self.returns), axis=1) ** 252 - 1
            )

        port_volatilities = np.array(
            [np.sqrt(np.dot(w.T, np.dot(self.cov_matrix, w))) for w in weights_matrix]
        )

        sharpe_ratios = (port_returns - self.risk_free_rate) / port_volatilities

        return pd.DataFrame(
            {
                "Return": port_returns,
                "Volatility": port_volatilities,
                "Sharpe Ratio": sharpe_ratios,
            }
        )

    def _minimize_volatility_obj(self, weights: np.ndarray) -> float:
        """Objective function to minimize portfolio volatility.

        Args:
            weights (np.ndarray): Portfolio weights.

        Returns:
            float: Portfolio volatility (only 1 item in the series).
        """

        # the objective function just needs to return a single floating-point value
        return self._calculate_portfolio_metrics(weights[np.newaxis, :])[
            "Volatility"
        ].iloc[0]

    # === Public methods ===#

    def monte_carlo_optimization(self) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
        """Performs Monte Carlo simulation to find the optimal portfolio weights.

        Returns:
            tuple[pd.DataFrame, pd.Series, pd.Series]: A tuple containing:
                - A DataFrame with the metrics of all simulated portfolios.
                - A Series with the metrics of the portfolio with the highest Sharpe ratio.
                - A Series with the metrics of the portfolio with the lowest volatility.
        """
        weights_matrix = self._generate_random_weights_matrix()

        results_df = self._calculate_portfolio_metrics(weights_matrix)

        for i, symbol in enumerate(self.returns.columns):
            results_df[f"Weight_{symbol}"] = weights_matrix[:, i]

        # Find portfolios with max Sharpe ratio and min volatility
        max_sharpe_portfolio = results_df.loc[results_df["Sharpe Ratio"].idxmax()]
        min_volatility_portfolio = results_df.loc[results_df["Volatility"].idxmin()]

        return results_df, max_sharpe_portfolio, min_volatility_portfolio

    def calculate_efficient_frontier(
        self, results_df: pd.DataFrame, n_points: int = 1000
    ):
        """Calculates the efficient frontier.

        Args:
            n_points (int): Number of points to calculate on the frontier.

        Returns:
            pd.DataFrame: A DataFrame containing the returns and volatilities of the efficient frontier portfolios.
        """
        # Define the range of target returns
        min_return = results_df["Return"].min()
        max_return = results_df["Return"].max()
        target_returns = np.linspace(min_return, max_return, n_points)

        efficient_portfolios = []

        for target in target_returns:
            # Define constraints
            constraints = (
                {"type": "eq", "fun": lambda w: np.sum(w) - 1},  # Sum of weights is 1
                {
                    "type": "eq",
                    "fun": lambda w: (np.dot(w, self.mean_returns) * 252) - target,
                },  # Portfolio return equals target
            )
            # Define bounds for each weight
            bounds = tuple((0, 1) for _ in range(self.n_assets))
            # Initial guess
            initial_weights = np.array([1.0 / self.n_assets] * self.n_assets)

            # Minimize volatility
            result = minimize(
                self._minimize_volatility_obj,
                initial_weights,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
            )

            if result.success:
                vol = result.fun
                efficient_portfolios.append({"Return": target, "Volatility": vol})

        return pd.DataFrame(efficient_portfolios)

    def calculate_cml(
        self,
        max_sharpe_portfolio: pd.Series,
        results_df: pd.DataFrame,
        x_axis_padding: float = 1.1,
    ) -> tuple[list, list]:
        """
        Calculates the Capital Market Line (CML).

        Args:
            max_sharpe_portfolio (pd.Series): The portfolio with the highest Sharpe ratio.
            results_df (pd.DataFrame): DataFrame with metrics of all simulated portfolios.
            x_axis_padding (float, optional): The padding to extend the CML on the x-axis.
                                             Defaults to 1.1.

        Returns:
            tuple[list, list]: A tuple containing the x and y coordinates for plotting the CML.
        """
        max_sharpe_vol = max_sharpe_portfolio["Volatility"]
        max_sharpe_ret = max_sharpe_portfolio["Return"]

        # The slope of the CML is the Sharpe Ratio of the tangency portfolio
        cml_slope = (max_sharpe_ret - self.risk_free_rate) / max_sharpe_vol

        cml_x = [0, results_df["Volatility"].max() * x_axis_padding]

        cml_y = [self.risk_free_rate, self.risk_free_rate + cml_slope * cml_x[1]]

        return cml_x, cml_y
