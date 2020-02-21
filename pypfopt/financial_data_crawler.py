#coding by Willhelm
import requests
import time
import pandas as pd
#sample query
#https://query1.finance.yahoo.com/v7/finance/download/0288.HK?period1=1546300800&period2=1577750400&interval=1d&events=history&crumb=UuO4UZuUbll


class financial_data_crawler(object):
    def __init__(self, stock_name, stock_code, local_data_add, cookies, crumb):
      '''
      Instance variables:
    



      Public methods:

      '''
      self.stock_name = stock_name
      self.stock_code = stock_code
      self.add = local_data_add
      self.cookies = cookies
      self.crumb = crumb
      self.query_head = "https://query1.finance.yahoo.com/v7/finance/download/"
      self.query_period1 = "?period1="
      self.query_period2 = "&period2="
      self.query_interval = "&interval="
      self.query_crumb = "&events=history&crumb="
      self.s = requests.Session()
    def crawle(self,start_date, end_date, interval, save_to_csv):
        # begin = datetime_timestamp("2014-01-01 09:00:00")

      for i in range(0,len(self.stock_code)):
        url = self.query_head+self.stock_code[i]+self.query_period1+start_date+self.query_period2+end_date+self.query_interval+interval+self.query_crumb
        data = self.s.get(url,cookies=self.cookies,verify=False)
        f = open(self.add+self.stock_name[i]+".csv",'w')
        f.write(data.text)
        f.close()


    def format_as_pypfopt_inputs(self, file_name):
        print("   ")