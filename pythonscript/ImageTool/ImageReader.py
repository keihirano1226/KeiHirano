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

imgfile = "cutImage_0000000000.png"
frame = cv2.imread(imgfile,cv2.IMREAD_ANYDEPTH)
print("dtype : " + str(frame.dtype))
cv2.imshow('test',frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
