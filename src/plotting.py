import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class PlottingUtil:
    """
    A utility class for creating common plots.
    """

    @staticmethod
    def plot_stock_performance(
        df: pd.DataFrame,
        x: str = "Date",
        y: str = "Close_normalized",
        hue: str = "Symbol",
        title: str = "Stock Price Performance (Normalized to Starting Value)",
        xlabel: str = "Date",
        ylabel: str = "Price Relative to Starting Value",
        figsize: tuple = (14, 6),
    ):
        """
        Plots the normalized stock price performance.

        Args:
            df (pd.DataFrame): DataFrame with processed stock data.
            x (str): Column name for the x-axis.
            y (str): Column name for the y-axis.
            hue (str): Column name for color encoding.
            title (str): Title of the plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            figsize (tuple): Figure size.
        """
        sns.set_style("whitegrid")
        plt.figure(figsize=figsize)

        sns.lineplot(
            data=df,
            x=x,
            y=y,
            hue=hue,
            linewidth=2,
        )

        plt.title(title, fontsize=16, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.legend(title=hue, bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_index_performance(
        df: pd.DataFrame,
        x: str = "Date",
        y_cols: list = [
            "Equal_Weighted_Index",
            "Price_Weighted_Index",
            "SP_500",
            "Value_Weighted_Index",
            "Risk_Parity_Index",
        ],
        title: str = "Index Performance Comparison",
        xlabel: str = "Date",
        ylabel: str = "Normalized Value",
        figsize: tuple = (14, 6),
    ):
        """
        Plots the normalized index performance for multiple indices.

        Args:
            df (pd.DataFrame): DataFrame with processed index data.
            x (str): Column name for the x-axis.
            y_cols (list): List of column names for the y-axis.
            title (str): Title of the plot.
            xlabel (str): Label for the x-axis.
            ylabel (str): Label for the y-axis.
            figsize (tuple): Figure size.
        """
        sns.set_style("whitegrid")
        plt.figure(figsize=figsize)

        for y_col in y_cols:
            sns.lineplot(data=df, x=x, y=y_col, label=y_col, linewidth=2)

        plt.title(title, fontsize=16, fontweight="bold")
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.legend(title="Index Type")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_portfolio_optimization_results(
        results: pd.DataFrame,
        efficient_frontier: pd.DataFrame,
        cml_x: list,
        cml_y: list,
        max_sharpe_portfolio: pd.Series,
        min_volatility_portfolio: pd.Series,
    ):
        """
        Plots the results of portfolio optimization, including the Efficient Frontier and Capital Market Line.

        Args:
            results (pd.DataFrame): DataFrame with portfolio simulation results.
            efficient_frontier (pd.DataFrame): DataFrame with efficient frontier data.
            cml_x (list): X-coordinates for the Capital Market Line.
            cml_y (list): Y-coordinates for the Capital Market Line.
            max_sharpe_portfolio (pd.Series): Data for the max Sharpe ratio portfolio.
            min_volatility_portfolio (pd.Series): Data for the min volatility portfolio.
        """
        sns.set_theme(style="white")
        plt.figure(figsize=(12, 7))

        sns.scatterplot(
            data=results,
            x="Volatility",
            y="Return",
            hue="Sharpe Ratio",
            palette="viridis",
            s=20,
            alpha=0.5,
            legend=False,
        )

        # Plot the Efficient Frontier
        plt.plot(
            efficient_frontier["Volatility"],
            efficient_frontier["Return"],
            "r--",
            linewidth=2,
            label="Efficient Frontier",
        )

        # Plot the CML
        plt.plot(cml_x, cml_y, "b-", linewidth=2, label="Capital Market Line (CML)")

        # Highlight the max Sharpe ratio portfolio
        plt.scatter(
            max_sharpe_portfolio["Volatility"],
            max_sharpe_portfolio["Return"],
            color="r",
            marker="*",
            s=250,
            edgecolors="black",
            label="Max Sharpe Ratio (Tangency Portfolio)",
        )

        # Highlight the min volatility portfolio
        plt.scatter(
            min_volatility_portfolio["Volatility"],
            min_volatility_portfolio["Return"],
            color="c",
            marker="X",
            s=150,
            edgecolors="black",
            label="Min Volatility Portfolio",
        )

        plt.title(
            "Efficient Frontier and Capital Market Line", fontsize=16, fontweight="bold"
        )
        plt.xlabel("Annualized Volatility", fontsize=12)
        plt.ylabel("Annualized Return", fontsize=12)
        plt.xlim(results["Volatility"].min() * 0.9, results["Volatility"].max() * 1.1)
        plt.ylim(results["Return"].min() * 0.9, results["Return"].max() * 1.1)
        plt.legend()
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        plt.show()

    @staticmethod
    def plot_full_optimization_results(
        results_df: pd.DataFrame,
        efficient_frontier: pd.DataFrame,
        cml_x: list,
        cml_y: list,
        min_vol_portfolio: pd.Series,
        mc_max_sharpe_portfolio: pd.Series,
        optimized_max_sharpe_portfolio: pd.Series,
    ):
        """
        Plots the results of portfolio optimization, highlighting the difference
        between the Monte Carlo and optimized tangency portfolios.

        Args:
            results_df (pd.DataFrame): DataFrame with portfolio simulation results.
            efficient_frontier (pd.DataFrame): DataFrame with efficient frontier data.
            cml_x (list): X-coordinates for the Capital Market Line.
            cml_y (list): Y-coordinates for the Capital Market Line.
            min_vol_portfolio (pd.Series): Data for the min volatility portfolio.
            mc_max_sharpe_portfolio (pd.Series): Data for the max Sharpe portfolio from Monte Carlo.
            optimized_max_sharpe_portfolio (pd.Series): Data for the max Sharpe portfolio from the optimizer.
        """
        sns.set_theme(style="white")
        plt.figure(figsize=(14, 8))

        # Plot the Monte Carlo simulation cloud
        sns.scatterplot(
            data=results_df,
            x="Volatility",
            y="Return",
            hue="Sharpe Ratio",
            palette="viridis",
            s=20,
            alpha=0.5,
            legend=False,
        )

        # Plot the Efficient Frontier
        plt.plot(
            efficient_frontier["Volatility"],
            efficient_frontier["Return"],
            "r--",
            linewidth=2,
            label="Efficient Frontier",
        )

        # Plot the CML (calculated using the *optimized* portfolio)
        plt.plot(cml_x, cml_y, "b-", linewidth=2, label="Capital Market Line (CML)")

        # Highlight the min volatility portfolio
        plt.scatter(
            min_vol_portfolio["Volatility"],
            min_vol_portfolio["Return"],
            color="c",
            marker="X",
            s=150,
            edgecolors="black",
            label="Min Volatility Portfolio",
        )

        # Highlight the max Sharpe portfolio from Monte Carlo
        plt.scatter(
            mc_max_sharpe_portfolio["Volatility"],
            mc_max_sharpe_portfolio["Return"],
            color="orange",
            marker="*",
            s=250,
            edgecolors="black",
            label="Max Sharpe (Monte Carlo Approx.)",
        )

        # Highlight the *optimized* max Sharpe portfolio (the true tangency portfolio)
        plt.scatter(
            optimized_max_sharpe_portfolio["Volatility"],
            optimized_max_sharpe_portfolio["Return"],
            color="r",
            marker="*",
            s=350,
            edgecolors="black",
            label="Max Sharpe (Optimized Tangency)",
        )

        plt.title(
            "Portfolio Optimization: Efficient Frontier & CML",
            fontsize=18,
            fontweight="bold",
        )
        plt.xlabel("Annualized Volatility (Risk)", fontsize=12)
        plt.ylabel("Annualized Return", fontsize=12)
        plt.xlim(left=0)
        plt.ylim(bottom=0)
        plt.legend(loc="best")
        plt.grid(True, alpha=0.2)
        plt.tight_layout()
        plt.show()
