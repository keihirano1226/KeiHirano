import pandas as pd
import numpy as np
import sys
import math
from sklearn.decomposition import PCA
from Normalize import centered

for j in range(1):
    csvfile = sys.argv[1] + "3dboneRotated" + str(j+1) + ".csv"
    df = pd.read_csv(csvfile)
    #進行方向の抽出
    Direction = df[["MidHipX","MidHipY",]]

    #進行方向行列に対して、正規化を行う。
    dfs = (Direction - Direction.mean()) / Direction.std()
    #主成分分析により、進行方向ベクトルを求める
    pca = PCA(n_components=1)
    feature = pca.fit(dfs)
    feature = pca.transform(dfs)
    print(pca.components_[0])
    print("test")
    #print(pca.components_[1])
    #c = np.dot(pca.components_[0])
    pca1 = pca.components_[0]
    print(pca1.shape)
    #2次元主成分軸の成す角度を計算する
    if j == 5:
        x = math.atan2(pca1[0],pca1[1])
    else:
        x = math.atan2(-pca1[0],-pca1[1])
    print(x)
    R = np.array([[math.cos(-x),-math.sin(-x),0],[math.sin(-x),math.cos(-x),0],[0,0,1]])
    #Data = pd.read_csv(Coordinate)
    body = df.drop(columns = "Frame")
    Time = df["Frame"]
    PoseMatrix = np.zeros(body.shape)
    for i in range(len(body)):
        df3 = body[i:i+1].values
        #1フレームの情報を一度25*3の行列に変換
        Frame = np.reshape(df3,(25,3))
        #Frame = -Origin + frame
        Pose = np.dot(R, Frame.T)
        Pose = Pose.T
        Pose = np.reshape(Pose,(1*75))
        PoseMatrix[i,:75] = Pose
    PoseData = pd.DataFrame(PoseMatrix)
    dfall = pd.concat([Time,PoseData],axis = 1)
    dfall.columns = df.columns
    dfall.to_csv(sys.argv[1] + "3dboneDirection" +str(j+1) + ".csv",index = 0)
    dfall2 = centered.JointCenter(dfall, "LWrist")
    dfall2.to_csv(sys.argv[1] + "Hino" +str(j+1) + ".csv")
