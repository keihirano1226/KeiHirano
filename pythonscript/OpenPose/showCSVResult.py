#出力の中身を確認するためのプログラム
# python3 showCSVResult.py 画像ファイルフォルダ　ファイルフォルダ
import glob
import json
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
from enum import Enum
import cv2
import numpy as np
import os
import csv
import pandas as pd

class JOINT(Enum):
    """
    #もともとの北村先生からもらってた関節リスト
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


csvFile = sys.argv[2]
imageFileList = glob.glob(sys.argv[1]+"/*")
imageFileList.sort()
df = pd.read_csv(csvFile,index_col = 0)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)

for i,imgFileName in enumerate(imageFileList):

    frame = cv2.imread(imgFileName,cv2.IMREAD_COLOR)
    print(type(frame))

    """
    jsonFile = open(jsonFileList[i] , 'r')
    jsonData = json.load(jsonFile)

    ver = float(jsonData['version'])
    Tag = "pose_keypoints"

    if ver == 1:
        Tag = "pose_keypoints"
    elif ver == 1.2:
        Tag = "pose_keypoints_2d"
    """


    peopleID = 0
    print("Frame #%d"%i)
    #csvの行を読み込んでそこだけ使うようにしたい
    #poseData = data[Tag]
    df1 = df[i:i+1]
    poseData = df1.values.tolist()
    #print(len(poseData))
    #poseData[JOINT.Neck.value*3], poseData[JOINT.Neck.value*3+1], poseData[JOINT.Neck.value*3+2] という書き方で関節の座標値やその座標値の信頼度を取得できる。
    """
    print("========People%d==============="%peopleID)
    for jointName in JOINT:
        index = jointName.value
        print(jointName.name,poseData[index*3],poseData[index*3+1],poseData[index*3+2]) # x,y,信頼度
    print("=================================")
    """

    kpt = np.array(poseData).reshape((25, 2))
    for p in jointPairs:
        pt1 = tuple(list(map(int, kpt[p[0], 0:2])))
        c1 = kpt[p[0], 1]
        pt2 = tuple(list(map(int, kpt[p[1], 0:2])))
        c2 = kpt[p[1], 1]
        # 信頼度0.0の関節は無視
        if c1 == 0.0 or c2 == 0.0:
            continue

        color = tuple(list(map(int, colors[0])))
        frame = cv2.line(frame, pt1, pt2, color, 7)
    #cv2.putText(frame,str(peopleID),(int(poseData[JOINT.Neck.value*2]),int(poseData[JOINT.Neck.value*2+1])),cv2.FONT_HERSHEY_PLAIN,2,(255,255,0))
    peopleID += 1
    cv2.imshow("img",frame)
    key = cv2.waitKey(0)
    if key == 27:
        break
