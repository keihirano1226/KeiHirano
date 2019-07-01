import pandas as pd
import numpy as np
import sys

csvpass = sys.argv[1] + "3dboneRotated.csv"
df = pd.read_csv(csvpass)
OpenPosecolumns = []
OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","RWrist","LWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate2 = ["X","Y","Z"]
for point in OpenPoseJoint:
    for coordinate in Coordinate2:
        newcolumn = point + coordinate
        OpenPosecolumns.append(newcolumn)
#print(body[OpenPosecolumns].shape)
selectedparts = df[OpenPosecolumns]
RightHand = selectedparts[["RWristX","RWristY","RWristZ"]]
PoseMatrix = np.zeros(selectedparts.shape)
for i in range(len(df)):
    df1 = selectedparts[i:i+1].values
    frame1 = np.reshape(df1,(int(selectedparts.shape[1]/3),3))
    frame1 = -RightHand[i:i+1].values + frame1
    Pose = np.reshape(frame1,(selectedparts.shape[1]))
    PoseMatrix[i,:selectedparts.shape[1]] = Pose
PoseData = pd.DataFrame(PoseMatrix)
PoseData.columns = OpenPosecolumns
print(PoseData)
PoseData.to_csv(sys.argv[1] + "GroundedPose.csv")
