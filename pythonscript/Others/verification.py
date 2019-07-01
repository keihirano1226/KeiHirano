import pandas as pd
import numpy as np
import pandas as pd
import sys
#三次元座標点郡の読み込み
groundDataPass = sys.argv[1] + "3points3D.csv"
Yaxispass = sys.argv[1] + "YaxisVec.csv"
Zaxispass = sys.argv[1] + "verticalPara.csv"
testpoints = sys.argv[1] + "Grid3D.csv"
df = pd.read_csv(groundDataPass,header = None)
original = df[1:2].values
yaxisdf = pd.read_csv(Yaxispass)
zaxisdf = pd.read_csv(Zaxispass)
yaxis = yaxisdf.values
zaxis = - zaxisdf.loc[:,["a","b","c"]].values
#zaxis = zaxisvec[]
yaxis1 = yaxis / np.linalg.norm(yaxis)
zaxis = zaxis / np.linalg.norm(zaxis)

xaxis = np.cross(yaxis1, zaxis)
xaxis = xaxis / np.linalg.norm(xaxis)
yaxis = np.cross(zaxis, xaxis)
yaxis = yaxis / np.linalg.norm(yaxis)
#print(xaxis)
#print(yaxis)
#print(zaxis)
#行列として、x,y,z軸を保存する
Rvector = np.r_[xaxis,yaxis,zaxis]
R = np.reshape(Rvector,(3, 3))
Gridpoints = pd.read_csv(testpoints,header = None)
i = 0
for i in range(len(Gridpoints)):
    df2 = Gridpoints[i:i+1].values
    Frame = -original + df2
    trans_Frame = np.dot(R, Frame.T)
    print(trans_Frame)
df2 = Gridpoints[4:].values
Frame = -original + df2
trans_Frame = np.dot(R, Frame.T)
print(trans_Frame)
