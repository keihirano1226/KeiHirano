import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm
#from Kinect_project import depth_projection


basepass = sys.argv[1]
imagepass = basepass + "/regi_mirror/" + "0000000060.jpg"
img = cv2.imread(imagepass)
df = pd.read_csv(basepass + "2DGround.csv", header = None)
points = df.values
for i in range(5):
    print(points[i:i+1])
    [[u,v]] = points[i:i+1]
    img = cv2.circle(img,(int(u),int(v)),5,(0,255,0))
    img = cv2.putText(img,str(i), (int(u),int(v)),cv2.FONT_HERSHEY_PLAIN,1.2,(0,0,255),1,cv2.LINE_AA)
cv2.imwrite(basepass + "2DGround.jpg",img)
