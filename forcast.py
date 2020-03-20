import pandas as pd
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from FCST.Read_Data import market_Dataset

reader = market_Dataset("C:\\Users\\willh\\Documents\\GitHub\\PyPortfolioOpt\\HSI_components_data\\^HSI.csv")
train = reader.read(package_length = 5)
trainloader = DataLoader(train,batch_size=4,shuffle=True)
print(len(dtrainloader))