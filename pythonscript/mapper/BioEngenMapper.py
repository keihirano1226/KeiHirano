import pandas as pd
import numpy as np
import sys
from uniframe import resampling as rs
import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score, davies_bouldin_score
import glob
from tqdm import tqdm

motionlist = glob.glob("/home/kei/document/experiments/BioEngen/ana/*_rotated.csv")
namelist = [2,3,6,7,9,11,14]
for motion in tqdm(motionlist):
    dfpose = pd.read_csv(motion)
    unidf = rs.dfSpline(dfpose, 500)
    motionpass_list = motion.split(".")
    unidf.to_csv(motionpass_list[0] + "_unified.csv" ,index = 0)
motion_num = 7
#距離行列計算用
OpenPoseJoint = ["RSholder","LSholder","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)
#各関節の距離行列の作成


RSholder_D = np.eye(motion_num)
LSholder_D = np.eye(motion_num)
MidHip_D = np.eye(motion_num)
RHip_D = np.eye(motion_num)
LHip_D = np.eye(motion_num)
RKnee_D = np.eye(motion_num)
LKnee_D = np.eye(motion_num)
RAnkle_D = np.eye(motion_num)
LAnkle_D = np.eye(motion_num)
Dis_Mat_list = (RSholder_D,LSholder_D,\
MidHip_D,RHip_D,LHip_D,RKnee_D,LKnee_D,RAnkle_D,LAnkle_D)
Unified_motion_list = glob.glob("/home/kei/document/experiments/BioEngen/ana/*_unified.csv")
print(Unified_motion_list)
col = 0
for Unified_motion in tqdm(Unified_motion_list):
    df = pd.read_csv(Unified_motion)
    pose = df[bodycolumns]
    row = 0
    for com_Unified_motion in tqdm(Unified_motion_list):
        df2 = pd.read_csv(com_Unified_motion)
        com_pose = df2[bodycolumns]
        Diff = pose - com_pose
        Diff_mat = Diff.values
        #採用する関節数が9個なので作成した差分行列を横軸方向に9個に分解
        Diff_mat_split = np.split(Diff_mat, 9, 1)
        #print(Diff_mat_split[0])
        j = 0
        for dis_mat in Dis_Mat_list:
            #各関節ごとの差分行列の積の体格成分から作成
            dis_mat[col:col+1,row:row+1] = np.sum(np.sqrt(np.diag(np.dot(Diff_mat_split[j],Diff_mat_split[j].T))))
            j+=1
        row+=1
    col+=1
joint_num = 0
Dis_all = np.zeros((motion_num,motion_num))
for dis_Mat in Dis_Mat_list:
    Dis_all += dis_Mat
    df_dis = pd.DataFrame(dis_Mat, columns = namelist, index = namelist)
    df_dis.to_csv("/home/kei/document/experiments/BioEngen/ana/result/" + OpenPoseJoint[joint_num] + "_dis.csv")
    joint_num+=1
Dis_all = pd.DataFrame(Dis_all, columns = namelist, index = namelist)
Dis_all.to_csv("/home/kei/document/experiments/BioEngen/ana/result/Distance.csv")
Distance = Dis_all.values
print(Distance)
darray = distance.squareform(Distance)
result = linkage(darray, method = "average")
"""
dendrogram(result,labels=namelist)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = 10 #フォントサイズを設定
plt.ylabel("distance")
plt.savefig("/home/kei/document/experiments/BioEngen/ana/result/elder.png")
"""
NUM_CLUSTERS_RANGE = range(2,7)
silhouette_coefficient = []
davies_bouldin_index = []
for num in NUM_CLUSTERS_RANGE:
    labels = fcluster(result, t=num, criterion='maxclust')
    silhouette_coefficient.append(silhouette_score(Distance, labels, metric='precomputed' ))
    davies_bouldin_index.append(davies_bouldin_score(Distance, labels))
p0, = plt.plot(NUM_CLUSTERS_RANGE, silhouette_coefficient, 'bo-', label='Silhouette Coefficient')
#p2, = par2.plot(NUM_CLUSTERS_RANGE, davies_bouldin_index, 'gs-', label='Davies Bouldin Index')
plt.xlabel('Number of Clusters')
plt.ylabel('Silhouette Coefficient')
#par2.set_ylabel('Davies Bouldin Index')
lines = [p0]
plt.legend(lines,
            [l.get_label() for l in lines],
            fontsize=10,
            bbox_to_anchor=(0, 0.1),
            loc='upper left')

plt.savefig("/home/kei/document/experiments/BioEngen/ana/result/シルエット係数.png")
