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

imageFileList = glob.glob(sys.argv[1]+"/*")
imageFileList.sort()

for i,imgFileName in enumerate(imageFileList):
    frame = cv2.imread(imgFileName,cv2.IMREAD_ANYDEPTH)
    #print(type(frame))
    #cv2.imshow('test',frame)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    dst = frame[1:1081,0:1920]
    number = str(i)
    title = 'cutImage_' + number.zfill(10) + '.png'
    print("dtype : " + str(dst.dtype))
    cv2.imwrite(title,dst)
