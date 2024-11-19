"""
This goal of this file is to be able to predict whether a team will pass or rush based on data available during a game

The expecation is that it is accurate enough to be valuable and fast enough to run between plays

"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from time import time
from PlayPredictionLoader import getData

# TODO move datasets to appropriate location

stopWatch = time()
X,y = getData()
print("Load Time: ", round(time()-stopWatch,5))

stopWatch = time()

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8)

clf = GaussianNB()

clf.fit(X_train, y_train)

print("Train Time: ", round(time()-stopWatch,5))

stopWatch = time()

acc = clf.score(X_test, y_test)

print("Test Time: ", round(time()-stopWatch,5))

#print(X.shape)
print("Accurarcy: ", round(acc*100,4))
