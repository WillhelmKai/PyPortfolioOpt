import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions, base_optimizer

import matplotlib
import matplotlib.pyplot as plt

# from pypfopt import boostrap

def modeling(t_set,boostrap=False, proportion=0):
  # Calculate expected returns and sample covariance
  if boostrap:
    mu, S= expected_returns.block_boostrap(t_set,proportion)
    # S = risk_models.sample_cov(t_set)
    # print(mu[0])
  else:
    mu = expected_returns.mean_historical_return(t_set)
    S = risk_models.sample_cov(t_set)
    # print(mu[0])
  # Optimise for maximal Sharpe ratio
  ef = EfficientFrontier(mu, S, gamma = 0)
  # raw_weights = ef.max_sharpe(risk_free_rate=0)
  ef.efficient_return(0.3)
  cleaned_weights = ef.clean_weights()
  expected_mu, expected_sigma, expected_sharpe = ef.portfolio_performance(verbose=False,risk_free_rate=0)
  return expected_mu, expected_sigma, expected_sharpe, cleaned_weights, ef

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


t_set = df[:int((9/12)*rows)]
v_set = df[int((9/12)*rows):]

expected_mu, expected_sigma, expected_sharpe, naive_weights,ef = modeling(t_set)
actual_mu, actual_sigma, actual_sharpe = testing(v_set,naive_weights)
_,_,_,no_averaged_weight,_= modeling(t_set)
print(naive_weights)

# name, temp = [],[]
# for w in naive_weights:
#     if naive_weights[w] != 0.0:
#         name += [w]
#         temp += [naive_weights[w]]
# fig1, ax1 = plt.subplots()
# ax1.set(title='Max Sharp Portfolio Weights without Boostrap')
# ax1.pie(temp, labels=name, autopct='%1.1f%%',startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# plt.show()

print("for Naive MK way")
print("Expected mu: %f, sigma: %f, sharpe %f" %(expected_mu, expected_sigma, expected_sharpe))
print("Actual mu: %f, sigma: %f, sharpe %f\n" %(actual_mu, actual_sigma, actual_sharpe))

T = 500
p = 0.5
mu, sigma, sharpe,  weight= [],[],[],np.zeros(num_of_stocks)
history = []
account = 0
for i in range(0,T):
  sample = t_set.sample(int(0.5*len(t_set)), replace = True)#.sort_values(by='Date')
  try:
    expected_mu, expected_sigma, expected_sharpe, cleaned_weights, ef = modeling(sample) #simple bootstrap method
    # expected_boostrap_mu, expected_boostrap_sigma, expected_boostrap_sharpe, boostrap_weights = modeling(t_set, True, proportion=0.5)
    
    mu += [expected_mu]
    sigma += [expected_sigma]
    sharpe += [expected_sharpe]
    weight += np.array(list(cleaned_weights.values()))
    history += [cleaned_weights]
    account+=1
  except Exception as e:
    continue


weight = weight/account
account = 0 
#transfer boostrap weight into format of naive weight and doing testing
for w in naive_weights:
  naive_weights[w] = weight[account]
  account+=1

print(naive_weights)

actual_mu, actual_sigma, actual_sharpe = testing(v_set,naive_weights)
print("Actual mu: %f, sigma: %f, sharpe %f\n" %(actual_mu, actual_sigma, actual_sharpe))


# name, temp = [],[]
# for w in naive_weights:
#     if naive_weights[w] > 0.0:
#         name += [w]
#         temp += [naive_weights[w]]
# fig1, ax1 = plt.subplots()
# ax1.set(title='Max Sharp Portfolio Weights with Boostrap')
# ax1.pie(temp, labels=name, autopct='%1.1f%%',startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.show()

# for w in naive_weights:
#     if naive_weights[w] != 0.0:
#         temp = []
#         for h in history:
#             temp += [h[w]]

#         fig, ax = plt.subplots()
#         ax.hist(np.array(temp), bins = 50)
#         ax.axvline(x=np.mean(np.array(temp)), color='r', linestyle='dashed', linewidth=2, label="Mean")
#         ax.axvline(x=np.array(no_averaged_weight[w]), color='b', linestyle='dashed', linewidth=2, label="Markowitz")
#         ax.set(xlabel='Weights (%)', ylabel='Frequency(1000 Times)',title='Max Sharp Portfolio Weights Distribution for '+str(w))
#         ax.legend()
#         fig.savefig(str(w)+".png")
        # plt.show()
        