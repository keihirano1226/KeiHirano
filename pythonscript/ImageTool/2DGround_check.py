import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
from Kinect_project import depth_projection

basepass = sys.argv[1]
imagepass = basepass + "/regi_mirror/" + "0000000200.jpg"
img = cv2.imread(imagepass)
df = pd.read_csv(basepass + "2DGround.csv", header = None)
points = df.values
projected_img = depth_projection(points,img)
cv2.imwrite(basepass + "2DGround.jpg",projected_img)
