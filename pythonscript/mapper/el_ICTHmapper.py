import pandas as pd
import numpy as np
import sys
from uniframe import resampling as rs
import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score, davies_bouldin_score

"""全部の動作を使った場合
subject2 = ((2,3,7,8),(4,5),(1,2,5,6,7))
subject3 = ((1,2,3,4,6),(1,2,3,4,5),(1,2,3,4,5))
subject4 = ((1,2,3,5,7),(1,2,3,7),(1,2,4,6,7))
"""
#1と3だけ使った場合


motionlist = ["SK1","SK2","SK3","SY2","SY3","SY4","SY5"]

for motion in motionlist:
    csvpass = sys.argv[1] + motion + ".csv"
    dfpose = pd.read_csv(csvpass)
    unidf = rs.dfSpline(dfpose, 200)
    unidf.to_csv(sys.argv[1] + "/Unified" + motion + ".csv",index = 0)
motion_num = 7
#距離行列計算用
OpenPoseJoint = ["Neck","LSholder","RElbow","LElbow","LWrist","RWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)
#各関節の距離行列の作成

Neck_D = np.eye(motion_num)
#RSholder_D = np.eye(motion_num)
LSholder_D = np.eye(motion_num)
RElbow_D = np.eye(motion_num)
LElbow_D = np.eye(motion_num)
RWrist_D = np.eye(motion_num)
LWrist_D = np.eye(motion_num)
MidHip_D = np.eye(motion_num)
RHip_D = np.eye(motion_num)
LHip_D = np.eye(motion_num)
RKnee_D = np.eye(motion_num)
LKnee_D = np.eye(motion_num)
RAnkle_D = np.eye(motion_num)
LAnkle_D = np.eye(motion_num)
Dis_Mat_list = (Neck_D,LSholder_D,RElbow_D,LElbow_D,RWrist_D,LWrist_D,\
MidHip_D,RHip_D,LHip_D,RKnee_D,LKnee_D,RAnkle_D,LAnkle_D)
col = 0
for motion in motionlist:
    csvpass = sys.argv[1] + "Unified" + motion + ".csv"
    df1 = pd.read_csv(csvpass)
    pose = df1[bodycolumns]
    row = 0
    for com_motion in motionlist:
        com_csvpass = sys.argv[1] + "Unified" + com_motion + ".csv"
        df2 = pd.read_csv(com_csvpass)
        com_pose = df2[bodycolumns]
        Diff = pose - com_pose
        Diff = Diff.abs()
        Diff_vec = Diff.sum()
        index = 0
        for dis_mat in Dis_Mat_list:
            dis_mat[col:col+1,row:row+1] = np.sqrt(Diff_vec[3*index]**2 + Diff_vec[3*index+1]**2 + Diff_vec[3*index+2]**2)
            index+=1
        row+=1
    col+=1
joint_num = 0
Dis_all = np.zeros((motion_num,motion_num))
for dis_Mat in Dis_Mat_list:
    Dis_all += dis_Mat
    df_dis = pd.DataFrame(dis_Mat, columns = motionlist, index = motionlist)
    df_dis.to_csv(sys.argv[1] + "/result/" + OpenPoseJoint[joint_num] + "_dis.csv")
    joint_num+=1
Dis_all = pd.DataFrame(Dis_all, columns = motionlist, index = motionlist)
Dis_all.to_csv(sys.argv[1] + "/result/Distance.csv")
df = pd.read_csv(sys.argv[1] + "/result/Distance.csv", index_col=0)
Distance = df.values
print(Distance.shape)
darray = distance.squareform(Distance)
print(darray)
print(darray.shape)
result = linkage(darray, method = "average")
print(result)
dendrogram(result,labels=df.columns)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = 10 #フォントサイズを設定
plt.title("Dendrogram")
plt.show()
