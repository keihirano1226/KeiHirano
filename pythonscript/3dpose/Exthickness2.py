import pandas as pd
import numpy as np
import sys

class body:
    def __init__(self,joint2d,joint3d,thickness):
        self.f = 365.2995
        self.c0 = 256.106689
        self.r0 = 208.944901
        self.pose2d = joint2d
        self.r = self.pose2d[0,0]
        self.c = self.pose2d[0,1]
        self.pose3d = joint3d
        self.thickness = thickness
    def Exthick(self):
        vector = np.array([self.c - self.c0,self.r - self.r0,self.f])
        thickness_vector = vector * self.thickness / np.linalg.norm(vector)
        return self.pose3d + thickness_vector
experimentpass = "/home/kei/document/experiments/" + sys.argv[1]
OpenPosefilepass = experimentpass + "output.csv"
Pose3Dpass = experimentpass + "3DInterrupt.csv"
bodythicknesspass = experimentpass + "bodythickness.csv"
df2d = pd.read_csv(OpenPosefilepass)
df3d = pd.read_csv(Pose3Dpass)
dfthick = pd.read_csv(bodythicknesspass)
df2d = df2d.drop("time",axis = 1)
df3d = df3d.drop("Frame",axis = 1)
print(df2d)
OpenPoseColumn = []
Pose3dColumn = []
bodycolumn = []
outputcolumns = df3d.columns
for i in range(25):
    OpenPoseColumn.append(2*i)
    OpenPoseColumn.append(2*i+1)
    Pose3dColumn.append(3*i)
    Pose3dColumn.append(3*i+1)
    Pose3dColumn.append(3*i+2)
    bodycolumn.append(i)
df2d.columns = OpenPoseColumn
df3d.columns = Pose3dColumn
dfthick.columns = bodycolumn
print(df2d)
i = 0
PoseMatrix = np.zeros(df3d.shape)
for i in range(len(df3d)):
    frame2d = df2d[i:i+1]
    frame3d = df3d[i:i+1]
    poseframe = np.zeros(frame3d.shape)
    print(poseframe.shape)
    print(i)
    j = 0
    for j in range(25):
        columns2d = [2*j,2*j+1]
        columns3d = [3*j,3*j+1,3*j+2]
        joint2d = frame2d.loc[:,columns2d].values
        joint3d = frame3d.loc[:,columns3d].values
        thickness = dfthick[j].values
        joint = body(joint2d,joint3d,thickness)
        print(str(j) + "番目の関節です")
        poseframe[0,3*j:3*j+3] = joint.Exthick()
    PoseMatrix[i,:75] = poseframe

PoseData = pd.DataFrame(PoseMatrix)
PoseData.columns = outputcolumns
PoseData.to_csv(experimentpass + "3DInterrupt2.csv")
