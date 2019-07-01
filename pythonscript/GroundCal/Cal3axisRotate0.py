import pandas as pd
import numpy as np
import sys

#垂直ベクトル,進行方向ベクトルを読み込み
csvfile1 = sys.argv[1] + "verticalPara.csv"
csvfile2 = sys.argv[1] + "DirectionVec.csv"
df1 = pd.read_csv(csvfile1)
df2 = pd.read_csv(csvfile2)

#データをベクトルに変換
verVec1 = -df1.values
verVec = verVec1[0:1,0:3]
print(verVec)
DirVec = df2.values
#進行方向を仮のx軸、鉛直方向をz軸として定義
TemXaxis = DirVec / np.linalg.norm(DirVec)
Zaxis = verVec / np.linalg.norm(verVec)

#仮のx軸とz軸から、外積を利用してy軸を計算
Yvec = np.cross(Zaxis, TemXaxis)
Yaxis = Yvec / np.linalg.norm(Yvec)

#y軸と、z軸から外積を利用して、真のx軸を再計算
Xvec = np.cross(Yaxis, Zaxis)
Xaxis = Xvec / np.linalg.norm(Xvec)

#行列として、x,y,z軸を保存する
Rvector = np.r_[Xaxis,Yaxis,Zaxis]
R = np.reshape(Rvector,(3, 3))
axisData = pd.DataFrame(R, index = ["X","Y","Z"], columns = ["x","y","z"])
axisData.to_csv(sys.argv[1] + "axisData.csv")

#体節位置座標データの読み込み
Coordinate = sys.argv[1] + "3DInterrupt.csv"
Data = pd.read_csv(Coordinate)
body = Data.drop(columns = "Frame")
Time = Data["Frame"]
print(body)
#地面のある一点を原点として座標変換を行うので、地面の一点を指定する
#地面座標を一点抽出してくる(この時、誤差が含まれた座標値であるので、注意)
GroundPass = sys.argv[1] + "3DGround.csv"
Ground = pd.read_csv(GroundPass)
point = Ground[:1].values
#point = np.array([[0.425195,-0.521684,1.407]])
print(point)
print(point.shape)
a = verVec1[0,0]
b = verVec1[0,1]
c = verVec1[0,2]
d = verVec1[0,3]
x0 = point[0,0]
y0 = point[0,1]
z0 = (-a*x0-b*y0-d)/c
Origin = np.array([x0,y0,z0])
print(Origin.shape)
PoseMatrix = np.zeros(body.shape)
for i in range(len(body)):
    df3 = body[i:i+1].values
    #1フレームの情報を一度25*3の行列に変換
    frame = np.reshape(df3,(25,3))
    Frame = -Origin + frame
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
