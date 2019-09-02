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
motionlist = ["SK1","SK2","SK3","SY2","SY3","SY4","SY5"]
df = pd.read_csv(sys.argv[1] + "/result/Distance.csv", index_col=0)
Distance = df.values
darray = distance.squareform(Distance)
result = linkage(darray, method = "average")
dendrogram(result,labels=df.columns)
#plt.title("Dendrogram")
#plt.show()

GT_labels = fcluster(result, t=2, criterion='maxclust')
OpenPoseJoint = ["Neck","LSholder","RElbow","LElbow","LWrist","RWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)

fscorelist = []
for joint in OpenPoseJoint:
    csvpass = sys.argv[1] + "/result/" + joint + "_dis.csv"
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
df_score_result.to_csv(sys.argv[1] + "/result/f_score.csv")
df_labels = pd.DataFrame(data = GT_labels, index = motionlist)
df_labels.to_csv(sys.argv[1] + "/result/label.csv")
csvpass = sys.argv[1] + "Unified" + motionlist[1] + ".csv"
dfpose = pd.read_csv(csvpass)
dfpose = dfpose[bodycolumns]
AveragePoseData = np.zeros((len(dfpose),len(dfpose.columns)))
AveragePose = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
i = 0
for motion in motionlist:
    csvpass = sys.argv[1] + "Unified" + motion + ".csv"
    dfpose = pd.read_csv(csvpass)
    dfpose = dfpose[bodycolumns]
    if df_labels.at[motion, 0] == 2:
        print(csvpass)
        print(dfpose)
        AveragePose += dfpose
        i+=1

AveragePose = AveragePose / i
AveragePose.to_csv(sys.argv[1] + "result/AveragePose2.csv")
