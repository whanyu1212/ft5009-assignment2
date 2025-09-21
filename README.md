# FT5009 Assignment 2: Market Analysis and Portfolio Optimization

### Methodology
**Sampling of 5 US-Listed Stocks**:

The more <u>robust and rigorous</u> way would to to do the following:

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

The workaround:

Due to the complexity and API rate limits associated with the rigorous method, a simplified approach was adopted . The five stocks were hand picked from the S&P 500 constituents, which inherently meets the large-cap requirement (minimum market cap of ~$22.7 billion).

-   **Negative-Return Stock**: Identified from publicly available financial news sources detailing long-term underperformers in the index (e.g., [S&P 500 Losers](https://www.benzinga.com/trading-ideas/long-ideas/25/08/47339739/sp-500-losers-22-stocks-negative-returns-10-years-getting-kicked-out)).
-   **Positive-Return Stocks**: Selected from well-known, high-growth sectors such as technology (e.g., FAANG stocks), which have demonstrated strong positive returns over the last decade.


The 5 stocks chosen are as follow:

| Symbol | 10-Year Return | Sector                 |
| :----- | :------------- | :--------------------- |
| VTRS   | Negative       | Healthcare             |
| GOOG   | Positive       | Technology             |
| AAPL   | Positive       | Technology             |
| META   | Positive       | Technology             |
| WMT    | Positive       | Consumer Staples       |

--- 
