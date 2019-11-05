import sys
import os
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import shutil
import pandas as pd
import re
from tqdm import tqdm
import numpy as np
basepass = sys.argv[1]
dx = sys.argv[2]

# os.mkdir(basepass + "regi_clean2")
# os.mkdir(basepass + "color2")

colorpass = glob.glob(basepass + "/regi_mirror/*.jpg")
colorpass.sort()
j = 0
for jpg_pass in tqdm(colorpass):
    im = cv2.imread(jpg_pass)
    rows= im.shape[0]
    cols = im.shape[1]
    M = np.float32([[1,0, dx],[0,1,0]])
    # M = np.float32([[1,0,25],[0,1,-10]])
    dst = cv2.warpAffine(im, M, (cols,rows))
    cv2.imwrite(basepass + "/regi_mirror_fixed/" + str(j).zfill(10) + ".jpg",dst)
    j+=1
