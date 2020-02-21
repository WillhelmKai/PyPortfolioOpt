import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

# Read in price data
add = "C:\\Users\\willh\\Documents\\GitHub\\PyPortfolioOpt\\HSI_components_data\\"
df = pd.read_csv(add+"HSI_components.csv", parse_dates=True, index_col="Date")

# Calculate expected returns and sample covariance
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimise for maximal Sharpe ratio
ef = EfficientFrontier(mu, S)
raw_weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()

print(cleaned_weights)
print("  ")
ef.portfolio_performance(verbose=True)
