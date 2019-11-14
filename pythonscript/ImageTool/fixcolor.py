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
#dx = sys.argv[2]
"""
os.mkdir(basepass + "regi2")
os.mkdir(basepass + "color2")
"""
colorpass = glob.glob(basepass + "/color/*.jpg")
colorpass.sort()
diff_vec = pd.read_csv(basepass + "diff_mean.csv", header= None)
#print(diff_vec)
fc = 1081.37207
fd = 366.335602
dx = round(diff_vec.iat[0,0]*fc/fd)
dy = round(diff_vec.iat[1,0]*fc/fd)
M = np.float32([[1,0,dx],[0,1,dy]])
print(M)
j = 0

for jpg_pass in tqdm(colorpass):
    im = cv2.imread(jpg_pass)
    rows= im.shape[0]
    cols = im.shape[1]
    dst = cv2.warpAffine(im, M, (cols,rows))
    cv2.imwrite(basepass + "/color2/" + str(j).zfill(10) + ".jpg",dst)
    j+=1
