#体の各体節の長さを1に正規化して，座標値を返却するスクリプト
import pandas as pd
import numpy as np
from enum import Enum
import sys

#2つの座標値セットを受け取って正規化したベクトル値を返却する
def Vec(ax,ay,az,bx,by,bz):
    b = np.array([bx.values,by.values,bz.values])
    a = np.array([ax.values,ay.values,az.values])
    vec0 = b-a
    vec = vec0 / np.linalg.norm(vec0)
    return vec

#必要なベクトルを受け取って各体の長さが1の骨盤を基準とする前進座標データを返却するためのスクリプト
def Pos(Frame,method):
    #胴体に関する情報
    if method ==  "OpenPose":
        SpineVec = Vec(Frame.MidHipX,Frame.MidHipY,Frame.MidHipZ,Frame.NeckX,Frame.NeckY,Frame.NeckZ)
        ClavicleL = Vec(Frame.NeckX,Frame.NeckY,Frame.NeckZ,Frame.LSholderX,Frame.LSholderY,Frame.LSholderZ)
        ClavicleR = Vec(Frame.NeckX,Frame.NeckY,Frame.NeckZ,Frame.RSholderX,Frame.RSholderY,Frame.RSholderZ)
        PelvisR = Vec(Frame.MidHipX,Frame.MidHipY,Frame.MidHipZ,Frame.RHipX,Frame.RHipY,Frame.RHipZ)
        PelvisL = Vec(Frame.MidHipX,Frame.MidHipY,Frame.MidHipZ,Frame.LHipX,Frame.LHipY,Frame.LHipZ)
        #腕に関する情報
        UpperarmR = Vec(Frame.RSholderX,Frame.RSholderY,Frame.RSholderZ,Frame.RElbowX,Frame.RElbowY,Frame.RElbowZ)
        UpperarmL = Vec(Frame.LSholderX,Frame.LSholderY,Frame.LSholderZ,Frame.LElbowX,Frame.LElbowY,Frame.LElbowZ)
        ForearmR = Vec(Frame.RElbowX,Frame.RElbowY,Frame.RElbowZ,Frame.RWristX,Frame.RWristY,Frame.RWristZ)
        ForearmL = Vec(Frame.LElbowX,Frame.LElbowY,Frame.LElbowZ,Frame.LWristX,Frame.LWristY,Frame.LWristZ)
        #足に関する情報
        FemurR = Vec(Frame.RHipX,Frame.RHipY,Frame.RHipZ,Frame.RKneeX,Frame.RKneeY,Frame.RKneeZ)
        FemurL = Vec(Frame.LHipX,Frame.LHipY,Frame.LHipZ,Frame.LKneeX,Frame.LKneeY,Frame.LKneeZ)
        ShinR = Vec(Frame.RKneeX,Frame.RKneeY,Frame.RKneeZ,Frame.RAnkleX,Frame.RAnkleY,Frame.RAnkleZ)
        ShinL = Vec(Frame.LKneeX,Frame.LKneeY,Frame.LKneeZ,Frame.LAnkleX,Frame.LAnkleY,Frame.LAnkleZ)

        #骨盤原点にして座標値を整理
        MidHip = np.zeros((1,3))
        Neck = SpineVec.T
        RSholder = SpineVec.T + ClavicleR.T
        RElbow = RSholder + UpperarmR.T
        RWrist = RElbow + ForearmR.T
        LSholder = SpineVec.T + ClavicleL.T
        LElbow = LSholder + UpperarmL.T
        LWrist = LElbow + ForearmL.T
        RHip = PelvisR.T
        RKnee = PelvisR.T + FemurR.T
        RAnkle = RKnee + ShinR.T
        LHip = PelvisL.T
        LKnee = PelvisL.T + FemurL.T
        LAnkle = LKnee + ShinL.T
        modiFrame = np.c_[Neck,RSholder,LSholder,RElbow,LElbow,RWrist,LWrist,MidHip,RHip,LHip,RKnee,LKnee,RAnkle,LAnkle]
        return modiFrame
def AllFrame(DataFrame,method):
    PoseMatrix = np.zeros((DataFrame.shape[0],42))
    for i in range(len(DataFrame)):
        df1 = DataFrame[i:i+1]
        test = Pos(df1,method)
        PoseMatrix[i:i+1] = test
    PoseData = pd.DataFrame(PoseMatrix)
    OpenPosecolumns = []
    OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","RWrist","LWrist","MidHip",\
    "RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
    Coordinate2 = ["X","Y","Z"]
    for point in OpenPoseJoint:
        for coordinate in Coordinate2:
            newcolumn = point + coordinate
            OpenPosecolumns.append(newcolumn)
    PoseData.columns = OpenPosecolumns
    return PoseData

if __name__ == '__main__':
    csvpass = "/home/kei/document/experiments/2019.06.06/frontwalk/3dboneRotated.csv"
    df = pd.read_csv(csvpass)
    PoseData_modi = AllFrame(df,"OpenPose")
    PoseData_modi.to_csv("/home/kei/document/KeiHirano/pythonscript/mapper/Normarized.csv",index = 0)
