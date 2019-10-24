#jsonfileを読み込んで一人の人の時系列データ行列に変換するためのコード
#python3 path/to/jsonfile directry
#入力 python3 csvposer.py path/to/experiment peopleID startframe endframe
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

isFixed = 1 #アフィン変換されているか否か

if isFixed:
    jsonFileList = glob.glob(sys.argv[1]+"/json_fixed/*")
    f1 = open(sys.argv[1] + '/output_fixed.csv','w')
    f2 = open(sys.argv[1] +'/probability_fixed.csv','w') 
else:
    jsonFileList = glob.glob(sys.argv[1]+"/json/*")
    f1 = open(sys.argv[1] + '/output.csv','w')
    f2 = open(sys.argv[1] +'/probability.csv','w')

jsonFileList.sort()
FocusedPeopleID = int(sys.argv[2])
#convertedfile= sys.argv[2] + "/converted"
#os.mkdir(convertedfile)
writer1 = csv.writer(f1, lineterminator='\n')
writer2 = csv.writer(f2, lineterminator='\n')
JointIndex = ['time']
probability_index = []
for joint in JOINT:
    #print(type(joint))
    JointIndex.append(joint.name + 'x')
    JointIndex.append(joint.name + 'y')
    probability_index.append(joint.name)
writer1.writerow(JointIndex)
writer2.writerow(probability_index)
current_Spine = np.zeros(4)
past_Spine = np.zeros(4)
StartFrame = int(sys.argv[3])
EndFrame = int(sys.argv[4])+1
for i in range(StartFrame, EndFrame):
    jsonFile = open(jsonFileList[i] , 'r')
    jsonData = json.load(jsonFile)

    ver = float(jsonData['version'])
    Tag = "pose_keypoints"

    if ver == 1:
        Tag = "pose_keypoints"
    else:
        Tag = "pose_keypoints_2d"

    peopleID = 0
    #print("Frame #%d"%i)
    if i == StartFrame:
        for data in jsonData['people']:
            poseData = data[Tag]
            twoDpose = []
            framelist = []#最終的にcsvに書き込みたい関節の座標値
            framelist.append(i)
            probabilitylist = []
            probability = []
            #一時的に読み込む2次元関節座標値
            for jointName in JOINT:
                #関節の位置を読み込むための区間
                index = jointName.value
                #print(jointName.name,poseData[index*3],poseData[index*3+1],poseData[index*3+2]) # x,y,信頼度
                twoDpose.append(poseData[index*3])
                twoDpose.append(poseData[index*3+1])
                probability.append(poseData[index*3+2])
            if peopleID == FocusedPeopleID:
                before2DposeData = twoDpose#前のフレームと比較する際に使うためのデータ
                beforeprob = probability
            peopleID = peopleID + 1
        twoDpose = before2DposeData
        framelist.extend(twoDpose)
        probabilitylist.extend(beforeprob)
        MinDistance = 1000
        #print(i)
        writer1.writerow(framelist)
        writer2.writerow(probabilitylist)
    else:
        for data in jsonData['people']:
            poseData = data[Tag]
            framelist = []#最終的にcsvに書き込みたい関節の座標値
            framelist.append(i)
            twoDpose = []#二次元関節座標値初期化
            probability = []#信頼度初期化
            probabilitylist = []
            for jointName in JOINT:
                #関節の位置を読み込むための区間
                index = jointName.value
                #print(jointName.name,poseData[index*3],poseData[index*3+1],poseData[index*3+2]) # x,y,信頼度
                twoDpose.append(poseData[index*3])
                twoDpose.append(poseData[index*3+1])
                probability.append(poseData[index*3+2])
            current_Neck = np.array([twoDpose[2],twoDpose[3]])
            current_pelvis = np.array([twoDpose[16],twoDpose[17]])
            current_Spine = np.concatenate((current_Neck,current_pelvis),axis = 0)#今見ている姿勢を格納する行列
            print(current_Spine)
            print(type(twoDpose))
            past_Neck = np.array([before2DposeData[2],before2DposeData[3]])
            past_pelvis = np.array([before2DposeData[16],before2DposeData[17]])
            past_Spine = np.concatenate((past_Neck,past_pelvis),axis = 0)
            print(past_Spine)
            DistanceVector = past_Spine - current_Spine
            #現在の他の関節の情報も取得する．
            #DistanceNorm = DistanceVector.flatten()
            Distance = np.linalg.norm(DistanceVector)
            #現在の他の関節の状況も鑑みて状況判断する．
            if Distance <= MinDistance:
                MinDistance = Distance
                #framelist = twoDpose
                min_probability = probability
                min_pose = twoDpose#最も前のフレームとの誤差が少なかった関節データで上書き
        framelist.extend(min_pose)
        probabilitylist.extend(min_probability)
        writer1.writerow(framelist)
        writer2.writerow(probabilitylist)
        if len(twoDpose) == 51:
            del twoDpose[50]
        before2DposeData = min_pose
        #前のフレームのデータを誤差最小二次元関節データで上書き
        print(before2DposeData)
        print(MinDistance)
        MinDistance = 1000
        print(i)
        print(type(min_pose))
        print(framelist)
f1.close()
f2.close()
