import glob
import sys
from PIL import Image, ImageOps
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import pandas as pd
imagepass = "/home/kei/document/experiments/Hamano/H5_1/regi_mirror/0000000127.jpg"
img = cv2.imread(imagepass,cv2.IMREAD_COLOR)
csvpass = "/home/kei/document/experiments/Hamano/H5_1/2DGround.csv"
df = pd.read_csv(csvpass,header=None)

mat = df.values
print(mat[0:1])
for i in range(len(df)):
    [[u,v]] = mat[i:i+1]
    print(u,v)
    img = cv2.circle(img,(int(u),int(v)),3,(0,255,0))
cv2.imwrite("/home/kei/document/experiments/Hamano/H5_1/test.jpg",img)
