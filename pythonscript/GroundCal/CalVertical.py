import pandas as pd
from sklearn import linear_model
import sys
import numpy as np
clf = linear_model.LinearRegression()

#三次元座標点郡の読み込み
groundDataPass = sys.argv[1] + "3DGround.csv"
df = pd.read_csv(groundDataPass)
"""
#三次元点群データ格納行列
data = df.values
mean = np.mean(data,axis = 0)
#[x-x0,y-y0,z-z0]の行列を作成する
dataX = data - mean
#特異値分解
u,s,v = np.linalg.svd(dataX)
nv = v[-1, :]
#サンプル点群の平面と原点との距離
ds = np.dot(data,nv)
param = np.r_[nv,-np.mean(ds)]
print(param.shape)
validata = np.insert(data,3,1,axis = 1)
print(validata)
distance = np.dot(validata,param.T)
print(distance)
print(distance.shape)
print(validata.shape)
"""

#~~~~~~~ちゃんとした最小二乗法でといた場合~~~~~~~~
data = df.values
df.columns = ['x','y','z']
#print(df)
z = df['z']
x1 = df.drop('z', axis=1)
x1['1'] = 1
t = z.values
X = x1.values
w = np.dot(np.linalg.inv(np.dot(X.T, X)), X.T)
w = np.dot(w,t)
#c = 1であると仮定
validata = np.insert(data,3,1,axis = 1)
param = np.array([-w[0],-w[1],1,-w[2]])
distance = np.dot(validata,param.T)#/(w[0]^2 + w[1]^2 + 1)^0.5
print(distance.shape)
norm = (w[0]**2 + w[1]**2 + 1)**0.5
l = [norm] * len(distance)
distance = distance / l
print("distance")
print(distance)
#~~~~~~~ちゃんとした最小二乗法でといた場合~~~~~~~~
dfsave = pd.Series(data=distance,name = 'distance(mm)', dtype='float')
dfsave.to_csv(sys.argv[1] + "distance.csv")
param = param.reshape([1,4])
Param = pd.DataFrame(param)
Param.columns = ["a","b","c","d"]
Param.to_csv(sys.argv[1] + "verticalPara.csv",index = 0)
"""
print(data)
print(dataX)
print(mean)
"""
