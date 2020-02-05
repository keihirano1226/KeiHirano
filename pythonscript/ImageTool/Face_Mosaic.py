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

def blackBox(src,x,y,width,height):
    if y+height <= src.shape[0] and x+width <= src.shape[1] and x >=0 and y>=0:
        src[y:y + height, x:x + width] =  np.zeros((height, width, 3), np.uint8)
        return src
    else:
        return src
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
Face = ["Nose","Neck","REye","LEye","REar","LEar"]
jointPairs = [(1,2), (1,5), (2,3), (3,4), (5,6), (6,7), (1,8), (8,9), (8,12), (9,10), (10,11), (11,24), (11,22), (22,23), (12,13), (13,14), (14,21),(14,19),(19,20)]
jsonFileList = glob.glob(sys.argv[1]+"/Face_json/*")
jsonFileList.sort()
imageFileList = glob.glob(sys.argv[1]+"/color_mirror/*")
imageFileList.sort()
for i,imageFileName in enumerate(imageFileList):
    print("hello")
    frame = cv2.imread(imageFileName,cv2.IMREAD_COLOR)
    print(i)
    jsonFile = open(jsonFileList[i], "r", encoding="utf-8")
    jsonData = json.load(jsonFile, encoding='utf-8')
    ver = float(jsonData['version'])
    Tag = "pose_keypoints"

    if ver == 1:
        Tag = "pose_keypoints"
    else:
        Tag = "pose_keypoints_2d"

    peopleID = 0
    for data in jsonData["people"]:
        poseData = data[Tag]
        #顔を囲うための左上を知るための行列
        a,b,c,d = 1920,1080,0,0
        Upper_left = np.array([a,b])
        #顔を囲うための右下を知るための行列
        Lower_right = np.array([c,d])
        for jointName in JOINT:
            index = jointName.value
            #顔の部品について画像内で撮影出来ている場合について処理の対象にする
            if jointName.name in Face and poseData[index*3+2]!=0:
                if poseData[index*3] <= a:
                    a = int(poseData[index*3])
                if poseData[index*3] >= c:
                    c = int(poseData[index*3])
                if poseData[index*3+1] <= b:
                    b = int(poseData[index*3+1])
                if poseData[index*3+1] >= d:
                    d = int(poseData[index*3+1])
                print(a,b,c,d)
        if a < c and b < d:
            frame = blackBox(frame,a-50,b-50,c-a+50,d-b+50)
        cv2.imwrite(sys.argv[1] + '/face/' + str(i).zfill(10) + '.jpg', frame)
