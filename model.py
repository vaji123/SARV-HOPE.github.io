# import pandas as pd 
# import numpy as np 
# from matplotlib import pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.ensemble import GradientBoostingClassifier

# df=pd.read_csv("spoon_marker.csv")

# #the id,date, column no need for analysis so drop it
# df1=df.drop(['ts','Date Time','Date','Time', 'cid','type'],axis=1)

# cdf = df1[['acx','acy','acz','gyx','gyY','gyz']]

# x = cdf.iloc[:, :6]
# y = cdf.iloc[:, -1]

# # kmean=KMeans(n_jobs = -1, n_clusters = 2, init='k-means++')
# # kmean.fit(x, y)

# kmean=GradientBoostingClassifier(n_estimators=150,max_depth=9)
# kmean.fit(x, y)

# import pandas as pd 
# import numpy as np 
# from matplotlib import pyplot as plt
# from sklearn.cluster import KMeans
# from sklearn.ensemble import GradientBoostingClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import accuracy_score

# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation


pima = pd.read_csv("data_spoon_marker.csv")
pima.head()
feature_cols = ['acx', 'acy', 'acz', 'gyx','gyY','gyz']
#label=['type']
X = pima[feature_cols] # Features
y = pima.type # Target variable
# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=5) # 70% training and 30% test
# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# pima = pd.read_csv("new_data_set_spoon_marker.csv")
# pima1=pima.drop(columns=['ts'],axis=1)

# pima_test3 = pd.read_csv("new_data_set_spoon_marker.csv")
# pima_test3.head()

# pima2=pima_test3.drop(columns=['Date Time','ts','Date','Time','cid','type'],axis=1)

# # shape of the dataset
# print('Shape of training data :',pima1.shape)
# print('Shape of testing data :',pima2.shape)

# # Now, we need to predict the missing target variable in the test data
# # target variable - Income

# # seperate the independent and target variable on training data
# train_x = pima1.drop(columns=['Date Time','Date','Time','cid','type'],axis=1)
# train_y = pima1['type']

 
# test_x = pima2[['gyY', 'gyz', 'gyx', 'acx', 'acy', 'acz']]
# #test_y = pima_test3['Income']

# #X_train, X_test, y_train, y_test = train_test_split(train_x, train_y, test_x, random_state=42)
# random_state=46

# model = GradientBoostingClassifier(n_estimators=150,max_depth=9)

# # fit the model with the training data
# model.fit(train_x,train_y)

# # predict the target on the train dataset
# predict_train = model.predict(train_x)
# print('\nTarget on train data',predict_train) 

# # Accuray Score on train dataset
# accuracy_train = accuracy_score(train_y,predict_train)
# print('\naccuracy_score on train dataset : ', accuracy_train)

# # predict the target on the test dataset
# predict_test = model.predict(test_x)
# print('\nTarget on test data',predict_test) 


# from sklearn.model_selection import cross_val_score

# dtree = DecisionTreeClassifier()
# mean_score = cross_val_score(dtree,pima2,predict_test, scoring="accuracy", cv = 7).mean()
# print(mean_score)




import pickle
pickle.dump(clf,open('new_prediction_1.pkl','wb'))