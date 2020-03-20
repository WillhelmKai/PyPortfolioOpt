#coding by Willhelm
import requests
import time
import pandas as pd
from sklearn import preprocessing
#sample query
#https://query1.finance.yahoo.com/v7/finance/download/0288.HK?period1=1546300800&period2=1577750400&interval=1d&events=history&crumb=UuO4UZuUbll


class market_Dataset(object):
    def __init__(self, path):
      '''
      Instance variables:
    



      Public methods:

      '''
      self.data_path = path

    def read(self,package_length):
      df = pd.read_csv(self.data_path, parse_dates=True, index_col="Date")
      # df = df.pct_change().dropna()

      #select adj_cloase, volume normalize
      df = df[['Adj Close','Volume']]
      scaler = preprocessing.StandardScaler().fit(df)
      mean, stdv = scaler.mean_, scaler.scale_
      df = scaler.transform(df)
      
      #devide three sets
      length = len(df)
      df_train, df_validation, df_testing = df[:int(length*0.6)],df[int(length*0.6)+1:int(length*0.8)],df[int(length*0.8)+1:]
      train, validation, testing = [],[],[]
      for i in range(0,len(df_train)-package_length-1):
        train+=[{"Input":df_train[i:i+package_length],"Target":df_train[i+package_length:i+package_length+1]}]

      for i in range(0,len(df_validation)-package_length-1):
        validation = [{"Input":df_validation[i:i+package_length],"Target":df_validation[i+package_length:i+package_length+1]}]
      
      for i in range(0,len(df_testing)-package_length-1):
        testing = [{"Input":df_testing[i:i+package_length],"Target":df_testing[i+package_length:i+package_length+1]}]
      
      # print(train)
      # print("  ")
      # print(df_testing.head())
      return train