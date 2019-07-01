import pandas as pd
import numpy as np
import sys

mocapfilepass = "/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "mocaptrans.csv"
mocap = pd.read_csv(mocapfilepass)
OpenPoseErrorpass = "/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "OpenPoseError.csv"
OpenPoseError = pd.read_csv(OpenPoseErrorpass)
mocapJoint = ["neck","Rshoulder","Lshoulder","Relbow","Lelbow","Rwrist","Lwrist","pelvis","RHip",\
"LHip","Rknee","Lknee","Rankle","Lankle"]
Coordinate = ["x","y","z"]
mocapcolumns = []
for point in mocapJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        mocapcolumns.append(newcolumn)
torsocolumns = []
torsomarkers = ["neck","Rshoulder","Lshoulder","Rpelvis",\
"Lpelvis","pelvis"]
FrontBack = ["F","B"]
for marker in torsomarkers:
    for plane in FrontBack:
        for coordinate in Coordinate:
            newcolumn = marker + plane + coordinate
            torsocolumns.append(newcolumn)

OpenPoseErrorcolumns = []
Method = ["OpenPose_"]#,"OpenPose_","OpenPoseBack_"]
ErrorJoint = ["Neck","RShoulder","Lshoulder","RElbow","LElobow","RWrist","LWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle","MPJPE"]
Distance = ["Euclidean"]
for method in Method:
    for point in ErrorJoint:
        for distance in Distance:
            newcolumn = method + point + distance
            OpenPoseErrorcolumns.append(newcolumn)
#これが胴体に貼付したマーカー変異
torso = mocap[torsocolumns]
#誤差の原因として，大きく乗っている誤差が体の厚みによるシフト誤差であるということを言うことが重要
Errors = OpenPoseError[OpenPoseErrorcolumns]

print(Errors.mean())
errormean = Errors.mean()
errorstd = Errors.std()
print(type(Errors))
print(type(errormean))
errormean1 = errormean.T
errorstd1 = errorstd.T
print(errormean1)
error = pd.concat([errormean,errorstd],axis = 1)
columns = ["mean","std"]
error.columns = columns
error.to_csv("./誤差平均と分散.csv")

#print(Errors.std)
