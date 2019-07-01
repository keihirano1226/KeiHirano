import pandas as pd
from sklearn import linear_model
import sys
import numpy as np
clf = linear_model.LinearRegression()

#三次元座標点郡の読み込み
groundDataPass = sys.argv[1] + "3points3d.csv"
df = pd.read_csv(groundDataPass,header = None)
original = df[0:1].values
x0 = df[1:2].values
y0 = df[2:].values
xvec = x0 - original
yvec = y0 - original
xaxis = xvec /np.linalg.norm(xvec)
yaxis1 = yvec /np.linalg.norm(yvec)
zaxis = np.cross(xaxis, yaxis1)
zaxis = -zaxis / np.linalg.norm(zaxis)
yaxis = np.cross(zaxis, xaxis)
print(xaxis)
print(yaxis)
print(zaxis)
#行列として、x,y,z軸を保存する
Rvector = np.r_[xaxis,yaxis,zaxis]
R = np.reshape(Rvector,(3, 3))

#体節位置座標データの読み込み
Coordinate = sys.argv[1] + "3DInterrupt.csv"
Data = pd.read_csv(Coordinate)
body = Data.drop(columns = "Frame")
Time = Data["Frame"]
print(body)
Origin = original
PoseMatrix = np.zeros(body.shape)
for i in range(len(body)):
    df3 = body[i:i+1].values
    #1フレームの情報を一度25*3の行列に変換
    frame = np.reshape(df3,(25,3))
    Frame = -original + frame
    Pose = np.dot(R, Frame.T)
    Pose = Pose.T
    Pose = np.reshape(Pose,(1*75))
    PoseMatrix[i,:75] = Pose
PoseData = pd.DataFrame(PoseMatrix)
dfall = pd.concat([Time,PoseData],axis = 1)
dfall.columns = Data.columns
dfall.to_csv(sys.argv[1] + "3dboneRotated.csv",index = 0)
print(Origin)
print(R)
