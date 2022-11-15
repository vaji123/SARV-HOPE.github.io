import pandas as pd 
import numpy as np 
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

df=pd.read_csv("RattleResults.csv")

#the id,date, column no need for analysis so drop it
df1=df.drop(['ts','Date Time','Date','Time', 'cid'],axis=1)

cdf = df1[['acx','acy','acz','gyx','gyY','gyz']]

x = cdf.iloc[:, :6]
y = cdf.iloc[:, -1]

kmean=KMeans(n_clusters = 2, init='k-means++')
kmean.fit(x, y)



import pickle
pickle.dump(kmean,open('kmeansArmwrap.pkl','wb'))