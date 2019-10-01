import pandas as pd
import numpy as np
import sys
from uniframe import resampling as rs
import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

df = pd.read_csv(sys.argv[1] + "1,3_result/Distance.csv", index_col=0)
Distance = df.values
darray = distance.squareform(Distance)
result = linkage(darray, method = "average")
dendrogram(result,labels=df.columns)
#plt.title("Dendrogram")
#plt.show()

GT_labels = fcluster(result, t=2, criterion='maxclust')
OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","LWrist","RWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)

fscorelist = []
for joint in OpenPoseJoint:
    csvpass = sys.argv[1] + "/1,3_result/" + joint + "_dis.csv"
    df_joint = pd.read_csv(csvpass, index_col=0)
    Distance_joint = df_joint.values
    darray_joint = distance.squareform(Distance_joint)
    result_joint = linkage(darray_joint, method = "average")
    pre_labels = fcluster(result_joint, t=2, criterion='maxclust')
    C_mat = confusion_matrix(GT_labels,pre_labels)
    f_score = f1_score(GT_labels,pre_labels)
    #print(f_score)
    fscorelist.append(f_score)

df_score_result = pd.DataFrame(data = fscorelist, index = OpenPoseJoint)
df_score_result.to_csv(sys.argv[1] + "1,3_result/f_score.csv")
df_labels = pd.DataFrame(data = GT_labels)
df_labels.to_csv(sys.argv[1] + "1,3_result/label.csv")
indexlist = []

i1 = 2
subject2 = ((2,3,7,8),(),(1,2,5,6,7))
subject3 = ((1,2,3,4,6),(),(1,2,3,4,5))
subject4 = ((1,2,3,5,7),(),(1,2,4,6,7))
motion_num = 29
subjectlist = (subject2, subject3,subject4)

for subject in subjectlist:
    j1 = 1
    for motion in subject:
        for num in motion:
            indexlist.append(str(i1) + "_" + str(j1) + "_" + str(num))
        j1 += 1
    i1 +=1
df_labels = pd.DataFrame(data = GT_labels, index = indexlist)
df_labels.to_csv(sys.argv[1] + "1,3_result/label.csv")
csvpass = sys.argv[1] + "subject" + str(2) + "/motion" + str(1) + "/" + str(2) + "/UnifiedPose.csv"
dfpose = pd.read_csv(csvpass)
dfpose = dfpose[bodycolumns]
AveragePoseData = np.zeros((len(dfpose),len(dfpose.columns)))
AveragePose = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
i = 0
for sub_index in indexlist:
    sub_num_list = sub_index.split("_")
    csvpass = sys.argv[1] + "subject" + sub_num_list[0] + "/motion" + sub_num_list[1] + "/" + sub_num_list[2] + "/UnifiedPose.csv"
    dfpose = pd.read_csv(csvpass)
    dfpose = dfpose[bodycolumns]
    if df_labels.at[sub_index, 0] == 1:
        AveragePose += dfpose
        i+=1

AveragePose = AveragePose / i
AveragePose.to_csv(sys.argv[1] + "1,3_result/AveragePose1.csv")
