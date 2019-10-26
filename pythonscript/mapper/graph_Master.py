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
import glob
import re
from tqdm import tqdm
from BodyColumn import Upper_joint as UJ
df = pd.read_csv(sys.argv[1] + "result/Distance.csv", index_col=0)
Distance = df.values
darray = distance.squareform(Distance)
result = linkage(darray, method = "average")
dendrogram(result,labels=df.columns)
#plt.title("Dendrogram")
#plt.show()

GT_labels = fcluster(result, t=2, criterion='maxclust')
"""
OpenPoseJoint = ["RSholder","LSholder","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle","RWrist",\
"RElbow","LElbow","LWrist"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)
"""
OpenPoseJoint,bodycolumns,Dis_Mat_list = UJ.Member(7)

fscorelist = []
for joint in OpenPoseJoint:
    csvpass = sys.argv[1] + "/UJ_result/" + joint + "_dis.csv"
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
df_score_result.to_csv(sys.argv[1] + "UJ_result/f_score.csv")
df_labels = pd.DataFrame(data = GT_labels)
df_labels.to_csv(sys.argv[1] + "UJ_result/label.csv")
indexlist = []
motionlist = glob.glob("/home/kei/document/experiments/Master/Unified/*.csv")
for motion in tqdm(motionlist):
    name_component = re.split("[./]", motion)
    indexlist.append(name_component[-2])


df_labels = pd.DataFrame(data = GT_labels, index = indexlist)
df_labels.to_csv(sys.argv[1] + "UJ_result/label.csv")
csvpass = sys.argv[1] + "Unified/H4_2.csv"
dfpose = pd.read_csv(csvpass)
dfpose = dfpose[bodycolumns]
AveragePoseData = np.zeros((len(dfpose),len(dfpose.columns)))
AveragePose = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
j = 0
i = 0
for sub_index in motionlist:
    dfpose = pd.read_csv(sub_index)
    dfpose = dfpose[bodycolumns]
    print(df_labels.at[indexlist[j], 0])
    if df_labels.at[indexlist[j], 0] == 1:
        print("hello")
        AveragePose += dfpose
        i+=1
    j+=1

AveragePose = AveragePose / i
AveragePose.to_csv(sys.argv[1] + "UJ_result/AveragePose1.csv")
