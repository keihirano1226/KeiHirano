import pandas as pd
import numpy as np
import sys
import glob
def CoordinateTra(df, Origin, R):
    body = df.drop(columns = "Frame")
    Time = df["Frame"]
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
    dfall.columns = df.columns
    return dfall

#垂直ベクトル,進行方向ベクトルを読み込み
csvfile1 = sys.argv[1] + "zaxis.csv"
csvfile2 = sys.argv[1] + "xaxis.csv"
csvfile3 = sys.argv[1] + "Origin.csv"
df1 = pd.read_csv(csvfile1)
df2 = pd.read_csv(csvfile2)
df3 = pd.read_csv(csvfile3, header = None)
Origin = df3.values

#データをベクトルに変換
verVec1 = -df1.values
verVec = verVec1[0:1,0:3]
print(verVec)
DirVec = -df2.values
DirVec = DirVec[0:1,0:3]
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
#Rvector = np.r_[Yaxis,Zaxis,Xaxis]
#Rvector = np.r_[Zaxis,Yaxis,-Xaxis]
Rvector = np.r_[Xaxis,Yaxis,Zaxis]
R = np.reshape(Rvector,(3, 3))
axisData = pd.DataFrame(R, index = ["X","Y","Z"], columns = ["x","y","z"])
axisData.to_csv(sys.argv[1] + "axisData.csv")
motion_list = glob.glob(sys.argv[1] + "MA*.csv")
for motion in motion_list:
    dfpose = pd.read_csv(motion)
    Pose_tra = CoordinateTra(dfpose, Origin, R)
    pass_list = motion.split(".")
    Pose_tra.to_csv(pass_list[0] + "_rotated.csv", index = 0)
"""
subject2 = ((2,3,7,8),(4,5),(1,2,5,6,7))
subject3 = ((1,2,3,4,6),(1,2,3,4,5),(1,2,3,4,5))
subject4 = ((1,2,3,5,7),(1,2,3,7),(1,2,4,6,7))

subjectlist = (subject2, subject3,subject4)
i = 2
for subject in subjectlist:
    j = 1
    for motion in subject:
        for num in motion:
            csvpass = sys.argv[1] + "subject" + str(i) + "/motion" + str(j) + "/" + str(num) + "/3DFiltered2.csv"
            print(csvpass)
            dfpose = pd.read_csv(csvpass)
            Pose_tra =  CoordinateTra(dfpose, Origin, R)
            Pose_tra.to_csv(sys.argv[1] + "subject" + str(i) + "/motion" + str(j) + "/" + str(num) + "/3dboneRotated.csv", index = 0)
        j+=1
    i+=1
"""
