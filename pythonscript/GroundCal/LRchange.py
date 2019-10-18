import pandas as pd
import numpy as np
import sys
import glob
#解析時に右手で触っているものと，左手で触っている動作を比較することが
#出来るように左手で手をついて立ち上がっているものは左右の反転を行い，
OpenPoseJoint = ["Nose","Neck","LSholder","LElbow",\
"LWrist","RSholder","RElbow","RWrist","MidHip",\
"LHip","LKnee","LAnkle","RHip","RKnee","RAnkle",\
"LEye","REye","LEar","REar","RBigToe","RSmallToe","RHeel",\
"LBigToe","LSmallToe","LHeel"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)
Folder_pass = sys.argv[1]
csvpass = Folder_pass + "3DFiltered.csv"
df = pd.read_csv(csvpass)
#回転させた行列と連結させるための処理
pose = df.Frame
df = df.drop("Frame",axis=1)
#左右反転のため，y軸の値を正負反転させる
R = np.array([[1,0,0],[0,-1,0],[0,0,1]])
for i in range(25):
    joint = df.iloc[:,[3*i,3*i+1,3*i+2]].values
    joint = joint.T
    rotated_joint = np.dot(R,joint)
