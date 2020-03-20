import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions, base_optimizer
# from pypfopt import boostrap

def modeling(t_set,boostrap=False, proportion=0):
  # Calculate expected returns and sample covariance
  if boostrap:
    mu, S= expected_returns.boostrap(t_set,proportion)
    # S = risk_models.sample_cov(t_set)
    print(mu[0])
  else:
    mu = expected_returns.mean_historical_return(t_set)
    S = risk_models.sample_cov(t_set)
    print(mu[0])
  # Optimise for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S, gamma = 0)
  raw_weights = ef.max_sharpe(risk_free_rate=0)

  cleaned_weights = ef.clean_weights()
  expected_mu, expected_sigma, expected_sharpe = ef.portfolio_performance(verbose=False)
  return expected_mu, expected_sigma, expected_sharpe, cleaned_weights

def testing(v_set,cleaned_weights):
  mu_v = expected_returns.mean_historical_return(v_set)
  S_v = risk_models.sample_cov(v_set)
  weights = np.fromiter(cleaned_weights.values(), dtype=float)
  actual_mu, actual_sigma, actual_sharpe = base_optimizer.portfolio_performance(mu_v,S_v,weights,False)

  return actual_mu, actual_sigma, actual_sharpe

# Read in price data
add = "C:\\Users\\willh\\Documents\\GitHub\\PyPortfolioOpt\\HSI_components_data\\"
df = pd.read_csv(add+"HSI_components.csv", parse_dates=True, index_col="Date")
df = df.where(pd.notnull(df), 54)
#for each set, calculate ef and weights
rows = len(df)
num_of_stocks = df.shape[1]


t_set = df[:int((11)*rows/12)]
v_set = df[int((11)*rows/12):]

expected_mu, expected_sigma, expected_sharpe, naive_weights = modeling(t_set)
actual_mu, actual_sigma, actual_sharpe = testing(v_set,naive_weights)

print(naive_weights)

print("for Naive MK way")
print("Expected mu: %f, sigma: %f, sharpe %f" %(expected_mu, expected_sigma, expected_sharpe))
print("Actual mu: %f, sigma: %f, sharpe %f\n" %(actual_mu, actual_sigma, actual_sharpe))

T = 10
p = 0.5
mu, sigma, sharpe,  weight = [],[],[],np.zeros(num_of_stocks)
for i in range(0,T):
  # sample = t_set.sample(int(n*len(t_set)), replace = True).sort_values(by=['Date'])

  # expected_mu, expected_sigma, expected_sharpe, cleaned_weights = modeling(sample)
  expected_boostrap_mu, expected_boostrap_sigma, expected_boostrap_sharpe, boostrap_weights = modeling(t_set, True, proportion=0.5)
  
  mu += [expected_boostrap_mu]
  sigma += [expected_boostrap_sigma]
  sharpe += [expected_boostrap_sharpe]
  weight += np.array(list(boostrap_weights.values()))

weight = weight/T
account = 0 
#transfer boostrap weight into format of naive weight and doing testing
for w in naive_weights:
  naive_weights[w] = weight[account]
  account+=1

print(naive_weights)

actual_mu, actual_sigma, actual_sharpe = testing(v_set,naive_weights)
print("Actual mu: %f, sigma: %f, sharpe %f\n" %(actual_mu, actual_sigma, actual_sharpe))

