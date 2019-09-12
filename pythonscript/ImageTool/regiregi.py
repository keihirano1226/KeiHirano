import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import shutil
import pandas as pd
import re
from tqdm import tqdm

basepass = sys.argv[1]
os.mkdir(basepass + "regi2")
os.mkdir(basepass + "color2")
colorpass = glob.glob(basepass + "color/*.jpg")
j = 0
for jpg_pass in tqdm(colorpass):
    im = cv2.imread(jpg_pass)
    rows,cols = im.shape
    M = np.float32([[1,0,15],[0,1,0]])
    dst = cv2.warpAffine(im, M, (cols,rows))
    cv2.imsave(basepass + "/color2/" + str(j).zfill(10) + ".jpg",color)
    j+=1
