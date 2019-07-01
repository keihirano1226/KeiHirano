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
import os
import csv
import re

#実験結果が入っているフォルダ
ResultFolder = sys.argv[1]
FrameFileName = sys.argv[1] + '2DFiltered.csv'
#os.mkdir(ResultFolder + "/Exdepth")
df = pd.read_csv(FrameFileName)
time = df.time
StartFrame = time[0]
EndFrame = time[len(df)-1]
ResultDepthFolder = sys.argv[1] + 'depth_mirror/*.tiff'
ImageFileList = glob.glob(ResultDepthFolder)
ImageFileList.sort()

for Image in ImageFileList:
    FileNameList = re.split('[./]',Image)
    FileNumber = int(FileNameList[-2])
    if (FileNumber <= EndFrame) and (StartFrame <= FileNumber):
        image = cv2.imread(Image,2)
        print(FileNumber)
        cv2.imwrite(ResultFolder + "/Exdepth/" + FileNameList[-2] + ".png", image)
