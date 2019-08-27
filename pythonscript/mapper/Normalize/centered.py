import pandas as pd
import numpy as np
import sys

def JointCenter(dataFrame, JointName):
    SelectedColumns = []
    dataFrame = dataFrame.drop("Frame", axis = 1)
    Coordinate2 = ["X","Y","Z"]
    for coordinate in Coordinate2:
        newcolumn = JointName + coordinate
        SelectedColumns.append(newcolumn)
    SelectedJoint = dataFrame[SelectedColumns]
    PoseMatrix = np.zeros(dataFrame.shape)
    for i in range(len(dataFrame)):
        df1 = dataFrame[i:i+1].values
        frame1 = np.reshape(df1,(int(dataFrame.shape[1]/3),3))
        frame1 = -SelectedJoint[i:i+1].values + frame1
        Pose = np.reshape(frame1,(dataFrame.shape[1]))
        PoseMatrix[i,:dataFrame.shape[1]] = Pose
    PoseData = pd.DataFrame(PoseMatrix)
    PoseData.columns = dataFrame.columns
    return PoseData

if __name__ == '__main__':
    csvpass = "/home/kei/document/experiments/ICTH2019/SY01/3dboneDirection.csv"
    df = pd.read_csv(csvpass)
    df2 = JointCenter(df, "RWrist")
    df2.to_csv("/home/kei/document/experiments/ICTH2019/SY01/JointCentered.csv")
