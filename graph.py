import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import objective_functions, base_optimizer
import matplotlib
import matplotlib.pyplot as plt
# from pypfopt import boostrap

def modeling(t_set,boostrap=False, proportion=0, target_return=0):
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
  ef = EfficientFrontier(mu, S, gamma = 0.9)
  # raw_weights = ef.max_sharpe(risk_free_rate=0)
  ef.efficient_return(target_return)
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


t_set = df[:int((11/12)*rows)]
v_set = df[int((11/12)*rows):]


#get the min return, max return and get the return 
mu_v = expected_returns.mean_historical_return(v_set)
S_v = risk_models.sample_cov(v_set)

mu = expected_returns.mean_historical_return(t_set)
S = risk_models.sample_cov(t_set)
ef = EfficientFrontier(mu, S, gamma = 0)
ef.min_volatility()
min_return, _, _ = ef.portfolio_performance(verbose=False,risk_free_rate=0)


max_return = 0.8
stride = 0.1
#cut the return into pieces 

print(min_return)

expected_mu, expected_sigma, a_mu, a_sigma, b_mu, b_sig = [],[],[],[],[],[]
for i in np.arange(min_return,max_return,stride):
    ef.efficient_return(i)
    re, sig, _ = ef.portfolio_performance(verbose=False,risk_free_rate=0)
    expected_mu += [re]
    expected_sigma += [sig]

    weights = np.fromiter(ef.clean_weights().values(), dtype=float)
    re, sig, _ = base_optimizer.portfolio_performance(mu_v,S_v,weights,False, risk_free_rate=0)
    a_mu += [re]
    a_sigma += [sig]

naive_weights = ef.clean_weights()



T = 100
p = 0.5
weights =dict()
acc = dict()
for j in np.arange(min_return,max_return,stride):
    weights[j] = np.zeros(num_of_stocks)
    acc[j] = 0


#each sample the data
for i in range(0,T):
    print(i/T)
    sample = t_set.sample(int(p*len(t_set)), replace = True)
    #using the data to calculate weights for every single return level
    for j in np.arange(min_return,max_return,stride):
        try:
            e_mu, e_sigma, e_sharpe, cleaned_weights, ef = modeling(sample,target_return=j)
            weights[j] += np.array(list(cleaned_weights.values()))
            acc[j] += 1
        except Exception as e:
            continue 


for w in weights:
    a = 0
    weights[w] = weights[w]/max(acc[w],1)
    for n in naive_weights:
        naive_weights[n] = weights[w][a]
        a += 1
    actual_mu, actual_sigma, _ = testing(v_set,naive_weights)
    b_mu +=[actual_mu]
    b_sig += [actual_sigma]

fig, ax = plt.subplots()
ax.plot(np.array(expected_sigma), np.array(expected_mu),'r',label='Expected PERF')
ax.plot(np.array(a_sigma), np.array(a_mu),label='Actual PERF')
ax.plot(np.array(b_sig), np.array(b_mu),label='Boostrap PERF',color='g')

ax.set(xlabel='Risk', ylabel='Return',
       title='Efficient Frontier')
ax.legend()

# fig.savefig("test.png")
plt.show()