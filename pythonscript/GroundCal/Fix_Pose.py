import pandas as pd
import numpy as np
import sys
basepath = sys.argv[1]
pose = pd.read_csv(basepath + "3DFiltered.csv",index_col = None)
Time = pose["Frame"]
allcolumns = pose.columns
pose = pose.drop("Frame",axis= 1)
point = pd.read_csv(basepath + "edge.csv",header= None)
point = point.values
point1 = pd.read_csv(basepath + "edge1.csv",header= None)
point1 = point1.values
R = pd.read_csv(basepath + "axisData.csv",index_col = 0)
R = R.values
PoseMatrix = np.zeros(pose.shape)
vec = point[0,:] - point1
Fix_vec = np.dot(R,vec.T )
print(Fix_vec.T.shape)
print(Fix_vec)

for i in range(len(pose)):
    df3 = pose[i:i+1].values
    #1フレームの情報を一度25*3の行列に変換
    frame = np.reshape(df3,(25,3))
    frame = frame.T
    vec = point[0,:] - point1
    Fix_vec = np.dot(R,vec.T )
    frame += Fix_vec
    Pose = frame.T
    Pose = np.reshape(Pose,(1*75))
    PoseMatrix[i,:75] = Pose
PoseData = pd.DataFrame(PoseMatrix)
dfall = pd.concat([Time,PoseData],axis = 1)
dfall.columns = allcolumns
dfall.to_csv(basepath + "3DFiltered1.csv",index = 0)
