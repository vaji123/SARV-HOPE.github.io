import numpy as np
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import  train_test_split


import warnings
import re
warnings.filterwarnings('ignore')

import pickle

data = pd.read_csv("RattleResults.csv")
data.head()


X,Y = data[['acx', 'acy', 'acz', 'gyx','gyY','gyz']], data[['cluster']]


# Splitting the dataset into train and test
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=.33, random_state=42)

#train model using gini index

tree = DecisionTreeClassifier(criterion = "gini", random_state = 35, max_depth=3, min_samples_leaf=2, 
                                  splitter="random", min_samples_split=5, max_features=None, max_leaf_nodes=None)
tree.fit(X_train, Y_train)

#model reuslts prediction
predicted = tree.predict(X_test)


import pickle
pickle.dump(tree,open('kmeansRattle.pkl','wb'))