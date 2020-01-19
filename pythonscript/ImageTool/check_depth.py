#クリックした点についてどこをクリックしたかをcsvファイルと画像を使って画像上に点を打つスクリプト
import pandas as pd
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

basePath = sys.argv[1]
imageFilePath = basePath + "/depth/0000000013.png"
Image = cv2.imread(imageFilePath)
csvpath = basePath + "depth_2d_points.csv"
csvpath2 = basePath + "regi_2d_points.csv"
df = pd.read_csv(csvpath,header=None)
df2 = pd.read_csv(csvpath2,header=None)
matrix = df.values
matrix2 = df2.values
for i in range(df.shape[0]):
    [u,v] = matrix[i]
    Image = cv2.circle(Image,(int(u),int(v)),5,(0,0,255))
    Image = cv2.putText(Image, str(i), (int(u),int(v)),cv2.FONT_HERSHEY_PLAIN,1.2,(0,0,255),1,cv2.LINE_AA)
cv2.imwrite(basePath + "/check_depth.jpg",Image)
diff = matrix - matrix2
df_diff = pd.DataFrame(data = diff, columns = ["r","c"])
mean_diff = df_diff.mean()
df_diff.to_csv(basePath + "diff.csv", index = False)
mean_diff.to_csv(basePath + "diff_mean.csv", index = False)
