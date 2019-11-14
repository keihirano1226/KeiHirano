#クリックした点についてどこをクリックしたかをcsvファイルと画像を使って画像上に点を打つスクリプト
import pandas as pd
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

basePath = sys.argv[1]
Image_num = sys.argv[2]
imageFilePath = basePath + "/regi/" + str(Image_num).zfill(10) + ".jpg"
Image = cv2.imread(imageFilePath)
csvpath = basePath + "regi_2d_points.csv"
df = pd.read_csv(csvpath,header=None)
matrix = df.values
for i in range(df.shape[0]):
    [u,v] = matrix[i]
    Image = cv2.circle(Image,(int(u),int(v)),5,(0,255,0))
    Image = cv2.putText(Image, str(i), (int(u),int(v)),cv2.FONT_HERSHEY_PLAIN,1.2,(0,0,255),1,cv2.LINE_AA)
cv2.imwrite(basePath + "/click.jpg",Image)
