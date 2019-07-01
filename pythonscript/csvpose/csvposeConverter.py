#jsonfileを読み込んで一人の人の時系列データ行列に変換するためのコード
#python3 path/to/jsonfile directry
#出力　output.csv(最新式のopenposeの出力を記録したもの)　outputcon.csv(これは旧式のopenposeの出力形式になるように変換を加えたもの)
import glob
import json
import sys
from enum import Enum
#import cv2
import numpy as np
import os
import csv
import pandas as pd
import numpy

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
    #Background = 25

class JOINTCON(Enum):
    Nose = 0
    Neck = 1
    RSholder = 2
    RElbow = 3
    RWrist = 4
    LSholder = 5
    LElbow = 6
    LWrist = 7
    RHip = 8
    RKnee = 9
    RAnkle = 10
    LHip = 11
    LKnee = 12
    LAnkle = 13
    REye = 14
    LEye = 15
    REar = 16
    LEar = 17



#jointPairs = [(1,2), (1,5), (2,3), (3,4), (5,6), (6,7), (1,8), (8,9), (9,10), (1,11), (11,12), (12,13), (1,0), (0,15), (15,17), (0,14), (14,16)]
#jointPairs = [(1,2), (1,5), (2,3), (3,4), (5,6), (6,7), (1,8), (8,9), (8,12), (9,10), (10,11), (11,24), (11,22), (22,23), (12,13), (13,14), (14,21),(14,19),(19,20)]
#colors = [(255.,     0.,    85.), (255.,     0.,     0.), (255.,    85.,     0.), (255.,   170.,     0.), (255.,   255.,     0.), (170.,   255.,     0.), (85.,   255.,     0.), (0.,   255.,     0.), (0.,   255.,    85.), (0.,   255.,   170.), (0.,   255.,   255.), (0.,   170.,   255.), (0.,    85.,   255.), (0.,     0.,   255.), (255.,     0.,   170.), (170.,     0.,   255.), (255.,     0.,   255.), (85.,     0.,   255.)]
#必要な列の組み合わせ(0~7,9~18)

jsonFileList = glob.glob(sys.argv[1]+"/json/*")
jsonFileList.sort()
FocusedPeopleID = int(sys.argv[2])
#convertedfile= sys.argv[2] + "/converted"
#os.mkdir(convertedfile)
f1 = open(sys.argv[1] + '/output.csv','w')
f2 = open('convertedoutput.csv','w')
writer1 = csv.writer(f1, lineterminator='\n')
writer2 = csv.writer(f2, lineterminator='\n')
JointIndex = ['time']
for joint in JOINT:
    #print(type(joint))
    JointIndex.append(joint.name + 'x')
    JointIndex.append(joint.name + 'y')
writer1.writerow(JointIndex)
for i in range(len(jsonFileList)):
    jsonFile = open(jsonFileList[i] , 'r')
    jsonData = json.load(jsonFile)

    ver = float(jsonData['version'])
    Tag = "pose_keypoints"

    if ver == 1:
        Tag = "pose_keypoints"
    elif ver == 1.2:
        Tag = "pose_keypoints_2d"

    peopleID = 0
    #print("Frame #%d"%i)
    if i == 0:
        for data in jsonData['people']:
            poseData = data[Tag]
            twoDpose = []
            framelist = []#最終的にcsvに書き込みたい関節の座標値
            framelist.append(i)
            #一時的に読み込む2次元関節座標値
            for jointName in JOINT:
                #関節の位置を読み込むための区間
                index = jointName.value
                #print(jointName.name,poseData[index*3],poseData[index*3+1],poseData[index*3+2]) # x,y,信頼度
                twoDpose.append(poseData[index*3])
                twoDpose.append(poseData[index*3+1])
            if peopleID == FocusedPeopleID:
                before2DposeData = twoDpose#前のフレームと比較する際に使うためのデータ
            peopleID = peopleID + 1
        twoDpose = before2DposeData
        framelist.extend(twoDpose)
        MinDistance = 1000
        #print(i)
        writer1.writerow(framelist)
    else:
        for data in jsonData['people']:
            poseData = data[Tag]
            framelist = []#最終的にcsvに書き込みたい関節の座標値
            framelist.append(i)
            twoDpose = []#初期化
            k = 0#初期化
            for jointName in JOINT:
                #関節の位置を読み込むための区間
                index = jointName.value
                #print(jointName.name,poseData[index*3],poseData[index*3+1],poseData[index*3+2]) # x,y,信頼度
                if poseData[index*3] == 0 or poseData[index*3 + 1] == 0 or abs(poseData[index*3] - before2DposeData[index*2]) >= 50 or (poseData[index*3+1] - before2DposeData[index*2+1]) >= 50:
                    #どちらか一方が0であれば、前のフレームの時の座標値と全く同じ値を埋めてフラグを立てる
                    twoDpose.append(before2DposeData[index*2])
                    twoDpose.append(before2DposeData[index*2 + 1])
                    k = k + 1
                elif poseData[index*3] != 0 and poseData[index*3 + 1] != 0:
                    twoDpose.append(poseData[index*3])
                    twoDpose.append(poseData[index*3+1])
                    #framelist.append(poseData[index*3])
                    #framelist.append(poseData[index*3+1])
            DistanceVector = np.array(twoDpose) - np.array(before2DposeData)
            #print(DistanceVector.shape)
            DistanceNorm = DistanceVector.flatten()
            Distance = np.linalg.norm(DistanceNorm)
            Distance = Distance*25/(25 - k)
            #隠れて見えなくなった関節の個数にあわせて誤差値を正規化
            if Distance <= MinDistance:
                MinDistance = Distance
                #framelist = twoDpose
                minpose = twoDpose#最も前のフレームとの誤差が少なかった関節データで上書き
        framelist.extend(minpose)
        writer1.writerow(framelist)
        if len(twoDpose) == 51:
            del twoDpose[50]
        before2DposeData = minpose
        #前のフレームのデータを誤差最小二次元関節データで上書き
        print(before2DposeData)
        print(MinDistance)
        MinDistance = 1000
        print(i)
        print(type(minpose))
        print(framelist)
f1.close()
df = pd.read_csv(sys.argv[1] + '/output.csv')
#print(df.Nosex)
j = 0
for joint2 in JOINTCON:

    IndexConx = joint2.name + 'x'
    IndexCony = joint2.name + 'y'
    print(IndexConx)
    df1 = df[IndexConx]
    df2 = df[IndexCony]
    if j == 0:
        dfc = pd.concat([df1,df2],axis=1)
    else:
        dfc = pd.concat([dfc,df1],axis=1)
        dfc = pd.concat([dfc,df2],axis=1)
    j = j + 1
dfc.to_csv(sys.argv[1] + "/outputcon.csv")
