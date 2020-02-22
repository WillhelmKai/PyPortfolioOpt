import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions, base_optimizer

# Read in price data
add = "C:\\Users\\willh\\Documents\\GitHub\\PyPortfolioOpt\\HSI_components_data\\"
df = pd.read_csv(add+"HSI_components.csv", parse_dates=True, index_col="Date")

#for each set, calculate ef and weights
rows = len(df)
for i in range(1,12):
  
  #perpare trainning and validation set
  t_set = df[int((i-1)*rows/12):int(i*rows/12)]
  v_set = df[int(i*rows/12)+1:int((i+1)*rows/12)]
  
  # Calculate expected returns and sample covariance
  mu = expected_returns.mean_historical_return(t_set)
  S = risk_models.sample_cov(t_set)

  # Optimise for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S)
  raw_weights = ef.max_sharpe()
  cleaned_weights = ef.clean_weights()

  print("===================")
  print("expected performance")
  ef.portfolio_performance(verbose=True)

  #perform validation
  mu_v = expected_returns.mean_historical_return(v_set)
  S_v = risk_models.sample_cov(v_set)
  weights = np.fromiter(cleaned_weights.values(), dtype=float)

  print("    ")
  print("actual performance")
  _,_, sharpe = base_optimizer.portfolio_performance(mu_v,S_v,weights,True)



#record actual return and variance

#average, sharpe rate

