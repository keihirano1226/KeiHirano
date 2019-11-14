# 入力 python showOpenPoseResult.py renderDir jsonDir
import glob
import json
import sys
from enum import Enum
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import numpy as np
import os
import csv
import pandas as pd
import codecs
from time import sleep

class JOINT(Enum):
    """もともとの北村先生からもらってた関節リスト
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
    """
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
jointPairs = [(1,2), (1,5), (2,3), (3,4), (5,6), (6,7), (1,8), (8,9), (8,12), (9,10), (10,11), (11,24), (11,22), (22,23), (12,13), (13,14), (14,21),(14,19),(19,20)]
colors = [(255.,     0.,    85.), (255.,     0.,     0.), (255.,    85.,     0.), (255.,   170.,     0.), (255.,   255.,     0.), (170.,   255.,     0.), (85.,   255.,     0.), (0.,   255.,     0.), (0.,   255.,    85.), (0.,   255.,   170.), (0.,   255.,   255.), (0.,   170.,   255.), (0.,    85.,   255.), (0.,     0.,   255.), (255.,     0.,   170.), (170.,     0.,   255.), (255.,     0.,   255.), (85.,     0.,   255.)]


jsonFileList = glob.glob(sys.argv[1]+"/json/*")
jsonFileList.sort()
imageFileList = glob.glob(sys.argv[1]+"/regi_mirror_fixed/*")
imageFileList.sort()

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

for i,imgFileName in enumerate(imageFileList):

    frame = cv2.imread(imgFileName,cv2.IMREAD_COLOR)
    print(type(frame))


    jsonFile = open(jsonFileList[i] , 'r', encoding='utf-8')
    jsonData = json.load(jsonFile, encoding='utf-8')

    ver = float(jsonData['version'])
    Tag = "pose_keypoints"

    if ver == 1:
        Tag = "pose_keypoints"
    else:
        Tag = "pose_keypoints_2d"

    peopleID = 0
    print("Frame #%d"%i)
#dataって変数によって順番にjsonfileの中身を読み込んでいる。
#pose_keypoints_2dを読みこんだらもう次の人のデータにアクセスする。
#読み込まれたファイルの中身は配列形式。
#このプログラムを変換して新しいjsonファイルを作成できるようにしたい。
#作成されたjsonファイルでは他のタグはいらない。
#jsonファイルの中身をソートするプログラムの作成が必要
#openpose_3dpose_sandbox.pyを変更して、jsonファイルではなく、関節をまとめたcsvファイルを参照するようにする。
    for data in jsonData['people']:
        poseData = data[Tag]
        #poseData[JOINT.Neck.value*3], poseData[JOINT.Neck.value*3+1], poseData[JOINT.Neck.value*3+2] という書き方で関節の座標値やその座標値の信頼度を取得できる。

        print("========People%d==============="%peopleID)
        for jointName in JOINT:
            index = jointName.value
            print(jointName.name,poseData[index*3],poseData[index*3+1],poseData[index*3+2]) # x,y,信頼度
        print("=================================")


        kpt = np.array(data[Tag]).reshape((25, 3))
        for p in jointPairs:
            j = 0
            pt1 = tuple(list(map(int, kpt[p[0], 0:2])))
            c1 = kpt[p[0], 2]
            pt2 = tuple(list(map(int, kpt[p[1], 0:2])))
            c2 = kpt[p[1], 2]
            # 信頼度0.0の関節は無視
            if c1 == 0.0 or c2 == 0.0:
                continue
            print(p)
            color = tuple(list(map(int, colors[0])))
            frame = cv2.line(frame, pt1, pt2, color, 7)
            j += 1
        cv2.putText(frame,str(peopleID),(int(poseData[JOINT.Neck.value*3]),int(poseData[JOINT.Neck.value*3+1])),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0))
        peopleID += 1
    cv2.imshow("img",frame)
    key = cv2.waitKey(0)
    if key == 27:
        break

print("SUCCESS!!")
print("Wait 5 seconds...")
sleep(5)
