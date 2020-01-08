import pandas as pd
import numpy as np
import sys
from CalProductaxis import vertical_detect

def vertical_detect(df):
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
    return param

basepath = sys.argv[1]
pose = pd.read_csv(basepath + "3DFiltered.csv",index_col = None)
Time = pose["Frame"]
allcolumns = pose.columns
pose1 = pose.drop("Frame",axis= 1)
csvfile1 = sys.argv[1] + "Zplane.csv"
csvfile2 = sys.argv[1] + "Xplane.csv"
df_z = pd.read_csv(csvfile1, header = None)
df_x = pd.read_csv(csvfile2, header = None)
zaxis = vertical_detect(df_z)
xaxis = vertical_detect(df_x)
#データをベクトルに変換
verVec = -zaxis[0:3]
DirVec = -xaxis[0:3]
#背もたれの法線ベクトルを仮のx軸、座面の鉛直方向をz軸として定義
TemXaxis = DirVec / np.linalg.norm(DirVec)
Zaxis = verVec / np.linalg.norm(verVec)

#仮のx軸とz軸から、外積を利用してy軸を計算
Yvec = np.cross(Zaxis, TemXaxis)
Yaxis = Yvec / np.linalg.norm(Yvec)

#y軸と、z軸から外積を利用して、真のx軸を再計算
Xvec = np.cross(Yaxis, Zaxis)
Xaxis = Xvec / np.linalg.norm(Xvec)

#行列として、x,y,z軸を保存する
#Rvector = np.r_[Yaxis,Zaxis,Xaxis]
#Rvector = np.r_[Zaxis,Yaxis,-Xaxis]
Rvector = np.r_[Xaxis,Yaxis,Zaxis]
R2 = np.reshape(Rvector,(3, 3))
R1 = pd.read_csv(basepath + "axisData.csv",index_col = 0)
R1 = R1.values
PoseMatrix = np.zeros(pose1.shape)
print(pose.shape)
for i in range(len(pose)):
    df3 = pose1[i:i+1].values
    #1フレームの情報を一度25*3の行列に変換
    frame = np.reshape(df3,(25,3))
    frame = frame.T
    tmp_pose = np.dot(R1.T,frame)
    rotated_pose = np.dot(R2,tmp_pose)
    Pose = rotated_pose.T
    Pose = np.reshape(Pose,(1,75))
    PoseMatrix[i,:75] = Pose
PoseData = pd.DataFrame(PoseMatrix)
dfall = pd.concat([Time,PoseData],axis = 1)
print(PoseData.shape)
dfall.columns = allcolumns
dfall.to_csv(basepath + "3DFiltered1.csv",index = 0)
