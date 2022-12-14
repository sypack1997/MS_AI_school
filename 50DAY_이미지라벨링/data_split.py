import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split
import pandas as pd


url = "https://raw.githubusercontent.com/mGalarnyk/Tutorial_Data/master/King_County/kingCountyHouseData.csv"
df = pd.read_csv(url)

columns = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'price']
features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors']
df = df.loc[:, columns]
# print(df.head(10))

X = df.loc[:, features] # image / shpae = [21613,5]
y = df.loc[:, ['price']] # label / shape = [21613,3]

x_train, x_test, y_train, y_test = train_test_split(X, y, random_state = 0, train_size=0.75)
# print(x_train.shape, x_test.shape) # shape = (16209,5) (5404,5)
# print(y_train.shape, y_test.shape) # shape = (16209,1) (5404,1)

