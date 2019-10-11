import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import shutil
import pandas as pd
import re
from tqdm import tqdm
import numpy as np
basepass = sys.argv[1]

os.mkdir(basepass + "regi2")
os.mkdir(basepass + "color2")

colorpass = glob.glob(basepass + "color/*.jpg")
colorpass.sort()
j = 0
for jpg_pass in tqdm(colorpass):
    im = cv2.imread(jpg_pass)
    rows= im.shape[0]
    cols = im.shape[1]
    M = np.float32([[1,0,0],[0,1,-15]])
    dst = cv2.warpAffine(im, M, (cols,rows))
    cv2.imwrite(basepass + "/color2/" + str(j).zfill(10) + ".jpg",dst)
    j+=1
