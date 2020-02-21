import requests
import pandas as pd
from pypfopt.financial_data_crawler import financial_data_crawler
#sample inquery
#https://query1.finance.yahoo.com/v7/finance/download/0288.HK?period1=1546300800&period2=1577750400&interval=1d&events=history&crumb=UuO4UZuUbll


stock_name = ["CKH HOLDINGS:00001.HK","CLP HOLDINGS:00002.HK",
"HK & CHINA GAS:00003.HK","HSBC HOLDINGS:00005.HK",
"POWER ASSETS:00006.HK","HANG SENG BANK:00011.HK",
"HENDERSON LAND:00012.HK","SHK PPT:00016.HK",
"NEW WORLD DEV:00017.HK","SWIRE PACIFIC:00019.HK",
"GALAXY ENT:00027.HK","MTR CORPORATION:00066.HK",
"SINO LAND:00083.HK","HANG LUNG PPT:00101.HK",
"WANT WANT CHINA:00151.HK","GEELY AUTO:00175.HK",
"CITIC:00267.HK","WH GROUP:00288.HK","SINOPEC CORP:00386.HK",
"HKEX:00388.HK","TECHTRONIC IND:00669.HK","CHINA OVERSEAS:00688.HK",
"TENCENT:00700.HK","CHINA UNICOM:00762.HK","LINK REIT:00823.HK",
"PETROCHINA:00857.HK","CNOOC:00883.HK","CCB:00939.HK",
"CHINA MOBILE:00941.HK","CKI HOLDINGS:01038.HK","HENGAN INT'L:01044.HK",
"CHINA SHENHUA:01088.HK","CSPC PHARMA:01093.HK",
"CHINA RES LAND:01109.HK","CK ASSET:01113.HK","SINO BIOPHARM:01177.HK",
"AIA:01299.HK","ICBC:01398.HK","SANDS CHINA LTD:01928.HK",
"WHARF REIC:01997.HK","COUNTRY GARDEN:02007.HK",
"AAC TECH:02018.HK","SHENZHOU INTL:02313.HK","PING AN:02318.HK",
"MENGNIU DAIRY:02319.HK","SUNNY OPTICAL:02382.HK",
"BOC HONG KONG:02388.HK","CHINA LIFE:02628.HK","BANKCOMM:03328.HK",
"BANK OF CHINA:03988.HK"] #%5EHSI


url1 = "https://query1.finance.yahoo.com/v7/finance/download/"
url2 = ".HK?period1=1546300800&period2=1577750400&interval=1d&events=history&crumb=UuO4UZuUbll"
add = "C:\\Users\\willh\\Documents\\GitHub\\PyPortfolioOpt\\HSI_components_data\\"
cookies = dict(B='c3kdcflervglj&b=3&s=mp')
crumb = "UuO4UZuUbll"
s = requests.Session()
#loop the name get the code and change the stock name
stock_code = list(stock_name)

for i in range(0,len(stock_name)):
  temp = stock_name[i]
  stock_code[i] = temp[temp.index(":")+2:temp.index(".HK")+3]
  stock_name[i] = temp[:temp.index(":")]

  # url = url1+stock_code[i]+url2
  # try:
  #   data = s.get(url,cookies=cookies,verify=False)
  # except Exception as e:
  #   print(stock_name[i])
  #   print(stock_code[i])
  #   print("  ")
  # f = open(add+stock_name[i]+".csv",'w')
  # f.write(data.text)
  # f.close()


# adj_close = []
# for i in range(0,len(stock_name)):
#   data = pd.read_csv(add+stock_name[i]+".csv",index_col=0,parse_dates=True, sep=",", dayfirst=True)
#   data = pd.DataFrame({stock_name[i] : data["Adj Close"][:]}) 
#   adj_close.append(data)

# adj_close = pd.concat(adj_close,axis=1)
# adj_close.to_csv(add+"HSI_components.csv")

crawler = financial_data_crawler(stock_name,stock_code,add,cookies,crumb)
crawler.crawle("1546300800","1577750400","1d", True)