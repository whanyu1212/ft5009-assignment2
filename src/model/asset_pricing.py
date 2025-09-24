import numpy as np
import pandas as pd
import statsmodels.api as sm


class AssetPricingModel:
    def __init__(self, df_returns: pd.DataFrame, risk_free_rate: float):
        self.df_returns = df_returns
        self.risk_free_rate = risk_free_rate

    def fit_capm_model(self):
        """Fits the CAPM model to estimate beta and alpha.
        Returns:
            dict: A dictionary containing beta, alpha, r_squared, p_value, and std_err.
        """
        # Prepare the data
        X = self.df_returns["Market_Excess_Return"]
        y = self.df_returns["Portfolio_Excess_Return"]
        X = sm.add_constant(X)  # Add a constant for the intercept (alpha)

        # Fit the linear regression model using OLS
        model = sm.OLS(y, X).fit()

        # Extract the results
        alpha, beta = model.params
        r_squared = model.rsquared
        p_values = model.pvalues
        std_err = model.bse

        return {
            "beta": beta,
            "alpha": alpha,
            "annualized_alpha": alpha * 252,  # Annualize alpha
            "r_squared": r_squared,
            "p_value_alpha": p_values[0],
            "p_value_beta": p_values[1],
            "std_err_alpha": std_err[0],
            "std_err_beta": std_err[1],
        }

    def fit_fama_french_3f_model(self, ff_factors: pd.DataFrame):
        """Fits the Fama-French 3-Factor model to estimate betas and alphas.
        Args:
            ff_factors (pd.DataFrame): DataFrame containing the Fama-French factors with columns:
                                       'Mkt-RF', 'SMB', 'HML', and 'RF'.
        Returns:
            dict: A dictionary containing betas, alpha, r_squared, p_values, and std_errs.
        """

        X = ff_factors[["Mkt-RF", "SMB", "HML"]]
        y = self.df_returns["Portfolio_Excess_Return"]
        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit()

        # Extract the results
        alpha = model.params[0]
        betas = model.params[1:]
        r_squared = model.rsquared
        p_values = model.pvalues
        std_errs = model.bse

        return {
            "betas": betas,
            "alpha": alpha,
            "annualized_alpha": alpha * 252,  # Annualize alpha
            "r_squared": r_squared,
            "p_value_alpha": p_values[0],
            "p_value_beta": p_values[1],
            "std_err_alpha": std_errs[0],
            "std_err_beta": std_errs[1],
        }

    def fit_carhart_4f_model(self, ff_momentum_factors: pd.DataFrame):
        """Fits the Carhart 4-Factor model to estimate betas and alphas.
        Args:
            ff_momentum_factors (pd.DataFrame): DataFrame containing the Fama-French factors with columns:
                                       'Mkt-RF', 'SMB', 'HML', 'MOM', and 'RF'.
        Returns:
            dict: A dictionary containing betas, alpha, r_squared, p_values, and std_errs.
        """

        X = ff_momentum_factors[["Mkt-RF", "SMB", "HML", "MOM"]]
        y = self.df_returns["Portfolio_Excess_Return"]
        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit()

        # Extract the results
        alpha = model.params[0]
        betas = model.params[1:]
        r_squared = model.rsquared
        p_values = model.pvalues
        std_errs = model.bse

        return {
            "betas": betas,
            "alpha": alpha,
            "annualized_alpha": alpha * 252,
            "r_squared": r_squared,
            "p_value_alpha": p_values[0],
            "p_value_beta": p_values[1],
            "std_err_alpha": std_errs[0],
            "std_err_beta": std_errs[1],
        }
