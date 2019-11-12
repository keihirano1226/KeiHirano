import pandas as pd
import sys
import csv
from enum import Enum

class JOINT(Enum):
    Nose = 0
    Neck = 1
    RSholder = 2
    RElbow = 3
    RWrist = 4
    LSholder = 5
    LElbow = 6
    LWrist = 7
    MidHip = 8
    RHip = 9
    RKnee = 10
    RAnkle = 11
    LHip = 12
    LKnee = 13
    LAnkle = 14
    REye = 15
    LEye = 16
    REar = 17
    LEar = 18
    LBigToe = 19
    LSmallToe = 20
    LHeel = 21
    RBigToe = 22
    RSmallToe = 23
    RHeel = 24

class Coordinate(Enum):
    X = 0
    Y = 1
    Z = 2

csvfile = sys.argv[1] + "save.csv"

columnname = list()
for joint in JOINT:
    for coordinate in Coordinate:
        column = joint.name + coordinate.name
        columnname.append(column)

df = pd.read_csv(csvfile, header = None)
df = df.drop(75, axis = 1)
#時間カラムの作成
Frame = list()
for i in range(df.shape[0]):
    frame = i
    Frame.append(frame)
s = pd.DataFrame(Frame, columns = ["Frame"])
df.columns = columnname
df = pd.concat([s, df], axis=1)
#print(df.shape[1])
#print(df)

df.to_csv(sys.argv[1] + "3dbone.csv", index = 0)

