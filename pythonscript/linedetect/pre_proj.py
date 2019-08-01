import pandas as pd
import numpy as np

csvfile = "/home/kei/document/experiments/KinectTest/randsave.csv"
df = pd.read_csv(csvfile)
dft = df.loc[:,["r","c","j"]]
dfX = df.loc[:,["x/z","y/z","z"]]
dfX["t"] = 1
dft["t"] = 1
X = dfX.values
t = dft.values
print(X)
print(t)
w1= np.dot(np.linalg.inv(np.dot(X.T, X)), X.T)
w = np.dot(w1,t)
point = np.dot(X,w)
print(point)
print(w.T)
