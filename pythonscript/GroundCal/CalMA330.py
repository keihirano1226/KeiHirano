import pandas as pd
import numpy as np
import sys
import glob
from sklearn.decomposition import PCA

def vertical_detect(df):
    data = df.values
    df.columns = ['x','y','z']
    #print(df)
    z = df['z']
    x1 = df.drop('z', axis=1)
    x1['1'] = 1
    t = z.values
    X = x1.values
    w = np.dot(np.linalg.inv(np.dot(X.T, X)), X.T)
    w = np.dot(w,t)
    #c = 1であると仮定
    validata = np.insert(data,3,1,axis = 1)
    param = np.array([-w[0],-w[1],1,-w[2]])
    return param

def CoordinateTra(df, Origin, R):
    body = df.drop(columns = "Frame")
    Time = df["Frame"]
    PoseMatrix = np.zeros(body.shape)
    for i in range(len(body)):
        df3 = body[i:i+1].values
        #1フレームの情報を一度25*3の行列に変換
        frame = np.reshape(df3,(25,3))
        Frame = -Origin + frame
        Pose = np.dot(R, Frame.T)
        Pose = Pose.T
        Pose = np.reshape(Pose,(1*75))
        PoseMatrix[i,:75] = Pose
    PoseData = pd.DataFrame(PoseMatrix)
    dfall = pd.concat([Time,PoseData],axis = 1)
    dfall.columns = df.columns
    return dfall

def Edge_detect(df):
    dfs = (df - df.mean()) / df.std()
    pca = PCA(n_components=1)
    feature = pca.fit(dfs)
    feature = pca.transform(dfs)
    edge_vec = pca.components_[0]
    return edge_vec
csvfile3 = sys.argv[1] + "edge.csv"
R = pd.read_csv(sys.argv[1] + "axisData.csv",index_col = 0)
R = R.values

df_edge = pd.read_csv(csvfile3, header = None)
Origin = df_edge[0:1].values

motion_list = glob.glob(sys.argv[1] + "MA*.csv")
for motion in motion_list:
    dfpose = pd.read_csv(motion)
    Pose_tra = CoordinateTra(dfpose, Origin, R)
    pass_list = motion.split(".")
    Pose_tra.to_csv(pass_list[0] + "_rotated.csv", index = 0)
