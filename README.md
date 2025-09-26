<!-- omit in toc -->
# FT5009 Assignment 2: Market Analysis and Portfolio Optimization

<!-- omit in toc -->
## Table of Content

- [Overview](#overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Methodology](#methodology)
- [Repo Structure](#repo-structure)

### Overview
This assignment encompasses an nalysis of a curated portfolio of five U.S.-listed stocks. The core objectives are as follows:

- **Performance Analysis**: Evaluate the historical performance of the selected stocks, both individually and in comparison to their respective market benchmarks.
- **Index Construction**: Develop and assess custom-weighted indices using the selected stocks, comparing their returns against established market indices.
- **Portfolio Optimization**:
    - Conduct a Monte Carlo simulation to optimize a portfolio composed of the three stocks with positive 10-year returns. This includes the visualization of the efficient frontier, the Global Minimum Variance (GMV) portfolio, and the Capital Market Line (CML).
    - Extend the optimization to a second portfolio that includes all five selected stocks.
- **CAPM Analysis**: Utilize the Capital Asset Pricing Model (CAPM) to calculate and interpret the alpha and beta values for the portfolios, providing insights into their risk-return characteristics.

### Getting Started

This section provides instructions on how to set up the project environment and install the necessary dependencies to run the analysis.

#### Prerequisites

-   **Python**: This project requires Python 3.10 or higher.
-   **uv**: The project uses `uv` for dependency management. You can install it by following the official [installation guide](https://github.com/astral-sh/uv).

#### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/whanyu1212/ft5009-assignment2.git
    cd ft5009-assignment2
    ```

2.  **Create a virtual environment**:
    It is recommended to create a virtual environment to isolate the project's dependencies.
    ```bash
    uv venv
    ```

3.  **Activate the virtual environment**:
    -   On macOS and Linux:
        ```bash
        source .venv/bin/activate
        ```
    -   On Windows:
        ```bash
        .venv\Scripts\activate
        ```

4.  **Install the dependencies**:
    Install all the required packages from `pyproject.toml`:
    ```bash
    uv sync
    ```

### Methodology
**Sampling of 5 US-Listed Stocks**:

Due to the complexity and API rate limits, she five stocks were hand picked from the S&P 500 constituents, which inherently meets the large-cap requirement (minimum market cap of ~$22.7 billion).

| Symbol | 10-Year Return | Sector                 |
| :----- | :------------- | :--------------------- |
| AAPL   | Positive       | Technology             |
| GOOG   | Positive       | Technology             |
| MSFT   | Positive       | Technology             |
| INTC   | Negative       | Semicon                |
| XOM    | Positive       | Energy                 |


<details>
<summary>The more <u>robust and rigorous</u> approach (click to expand)</summary>

1.  **Data Acquisition**:
    -   Fetch a complete list of US-listed stocks (e.g., NYSE, NASDAQ) using the Alpha Vantage `Listing & Delisting Status` endpoint.
    -   For each stock, retrieve its market capitalization (Both Alpha Vantage and YFinance provides this but Alpha Vantage's rate limit is only 25 per day for free users).

2.  **Initial Filtering**:
    -   Filter the list to include only stocks with a market capitalization greater than $10 billion.

3.  **Performance-Based Categorization**:
    -   Divide the filtered stocks into two distinct groups:
        -   `Positive-Return Group`: Stocks with positive 10-year returns.
        -   `Negative-Return Group`: Stocks with negative 10-year returns.

4.  **Sector-Diverse Selection Process**:

    -   **Select One `Negative-Return` Stock**:
        -   Randomly select one sector from the `Negative-Return Group`.
        -   Randomly pick one stock from the chosen sector.

    -   **Select Three `Positive-Return` Stocks**:
        -   Identify all sectors in the `Positive-Return Group` that have not yet been selected.
        -   Randomly choose three of these unique sectors.
        -   From each of the three chosen sectors, randomly select one stock.

    -   **Select Final `Positive-Return` Stock**:
        -   From the remaining unselected sectors in the `Positive-Return Group`, randomly choose one more sector.
        -   Randomly pick one stock from this final sector.

5.  **Final Portfolio**:
    -   Combine the five selected stocks to form the final sample portfolio.
</details>

---

### Repo Structure

The repository is organized into a modular structure to separate concerns and enhance maintainability. The core logic is encapsulated within the `src` directory, which is further divided into the following components:

-   **`config.py`**: A centralized configuration file using `dataclasses` to define and manage immutable settings for the analysis, such as the list of stocks, date ranges, and financial constants.

-   **`data/`**: This module is responsible for all data-related operations, including fetching, processing, and calculating metrics.
    -   `loaders/`: Contains data loaders for fetching financial data from external APIs. The primary loader is `yf_loader.py` for Yahoo Finance.
    -   `processing/`: Includes the `DataProcessor` class, which cleans the raw data, calculates returns, and normalizes prices.
    -   `metrics/`: Houses calculators for financial metrics, such as the `AnnualizedMetricsCalculator` for annualized returns and volatility.

-   **`index/`**: This component is dedicated to constructing various types of market indices.
    -   `IndexBuilder`: A class that builds equal-weighted, price-weighted, value-weighted, and risk-parity indices from the processed stock data.

-   **`model/`**: Contains implementations of financial models.
    -   `AssetPricingModel`: A class for applying asset pricing models like the Capital Asset Pricing Model (CAPM) to evaluate portfolio performance.

-   **`portfolio/`**: This module focuses on portfolio optimization and analysis.
    -   `PortfolioOptimizer`: Implements portfolio optimization using Monte Carlo simulation to find the efficient frontier, the tangency portfolio (max Sharpe ratio), and the minimum variance portfolio.

-   **`plotting.py`**: A utility class with static methods for creating various plots, such as stock performance, index comparisons, and the efficient frontier, using `matplotlib` and `seaborn`.
