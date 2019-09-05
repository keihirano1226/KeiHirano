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
subject2 = ((2,3,7,8),(),(1,2,5,6,7))
subject3 = ((1,2,3,4,6),(),(1,2,3,4,5))
subject4 = ((1,2,3,5,7),(),(1,2,4,6,7))

motion_num = 29
subjectlist = (subject2, subject3,subject4)

i = 2
for subject in subjectlist:
    j = 1
    for motion in subject:
        for num in motion:
            csvpass = sys.argv[1] + "subject" + str(i) + "/motion" + str(j) + "/" + str(num) + "/3dboneRotated.csv"
            print(csvpass)
            dfpose = pd.read_csv(csvpass)
            unidf = rs.dfSpline(dfpose, 200)
            unidf.to_csv(sys.argv[1] + "subject" + str(i) + "/motion" + str(j) + "/" + str(num) + "/UnifiedPose.csv",index = 0)

        j+=1
    i+=1

#距離行列計算用
OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","LWrist","RWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)
#各関節の距離行列の作成

Neck_D = np.eye(motion_num)
RSholder_D = np.eye(motion_num)
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
Dis_Mat_list = (Neck_D,RSholder_D,LSholder_D,RElbow_D,LElbow_D,RWrist_D,LWrist_D,\
MidHip_D,RHip_D,LHip_D,RKnee_D,LKnee_D,RAnkle_D,LAnkle_D)
i1 = 2
col = 0
indexlist = []
for subject in subjectlist:
    #全被験者のうちのある被験者(subject)
    j1 = 1
    for motion in subject:
        #ある被験者のうちのある座り方(motion)
        for num in motion:
            #ある座り方のうちnum試行目
            csvpass = sys.argv[1] + "subject" + str(i1) + "/motion" + str(j1) + "/" + str(num) + "/UnifiedPose.csv"
            df1 = pd.read_csv(csvpass)
            pose = df1[bodycolumns]
            i2 = 2
            row = 0
            indexlist.append(str(i1) + "_" + str(j1) + "_" + str(num))
            for com_subject in subjectlist:
                j2 = 1
                for com_motion in com_subject:
                    for com_num in com_motion:
                        com_csvpass = sys.argv[1] + "subject" + str(i2) + "/motion" + str(j2) + "/" + str(com_num) + "/UnifiedPose.csv"
                        print(com_csvpass)
                        df2 = pd.read_csv(com_csvpass)
                        com_pose = df2[bodycolumns]
                        Diff = pose - com_pose
                        Diff = Diff.abs()
                        Diff_vec = Diff.sum()
                        index = 0
                        for dis_mat in Dis_Mat_list:
                            print(Diff_vec[index])
                            dis_mat[col:col+1,row:row+1] = np.sqrt(Diff_vec[3*index]**2 + Diff_vec[3*index+1]**2 + Diff_vec[3*index+2]**2)
                            index+=1
                        row += 1
                    j2 += 1
                i2 += 1
            col += 1
        j1+=1
    i1+=1
joint_num = 0
Dis_all = np.zeros((motion_num,motion_num))
for dis_Mat in Dis_Mat_list:
    Dis_all += dis_Mat
    df_dis = pd.DataFrame(dis_Mat, columns = indexlist, index = indexlist)
    df_dis.to_csv(sys.argv[1] + "1,3_result/" + OpenPoseJoint[joint_num] + "_dis.csv")
    joint_num+=1
Dis_all = pd.DataFrame(Dis_all, columns = indexlist, index = indexlist)
Dis_all.to_csv(sys.argv[1] + "1,3_result/Distance.csv")

df = pd.read_csv(sys.argv[1] + "1,3_result/Distance.csv", index_col=0)
Distance = df.values
print(Distance.shape)
darray = distance.squareform(Distance)
print(darray)
print(darray.shape)
result = linkage(darray, method = "average")
print(result)
dendrogram(result,labels=df.columns)
# plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = 10 #フォントサイズを設定
plt.title("Dendrogram")
# plt.show()
plt.savefig("./test.png")

NUM_CLUSTERS_RANGE = range(2,motion_num)
silhouette_coefficient = []
davies_bouldin_index = []
for num in NUM_CLUSTERS_RANGE:
    labels = fcluster(result, t=num, criterion='maxclust')
    silhouette_coefficient.append(silhouette_score(Distance, labels, metric='precomputed' ))
    davies_bouldin_index.append(davies_bouldin_score(Distance, labels))

fig = plt.figure()
host = fig.add_subplot(111)
par2 = host.twinx()

p0, = host.plot(NUM_CLUSTERS_RANGE, silhouette_coefficient, 'bo-', label='Silhouette Coefficient')
#p2, = par2.plot(NUM_CLUSTERS_RANGE, davies_bouldin_index, 'gs-', label='Davies Bouldin Index')
host.set_xlabel('Number of Clusters')
host.set_ylabel('Silhouette Coefficient')
#par2.set_ylabel('Davies Bouldin Index')
lines = [p0]
host.legend(lines,
            [l.get_label() for l in lines],
            fontsize=10,
            bbox_to_anchor=(0, 0.1),
            loc='upper left')

fig.savefig(sys.argv[1] + "test.png")