import pandas as pd
import numpy as np
import sys
import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score, davies_bouldin_score
from tqdm import tqdm
from BodyColumn import body_columns as bc
from subject_list import subjectlist, motion_num

df = pd.DataFrame()
print("被験者データ読み込み中...")
for subject_index, subject in enumerate(tqdm(subjectlist), 2):
    #全被験者のうちのある被験者(subject)
    for motion_index, motion in enumerate(subject,1):
        #ある被験者のうちのある座り方(motion)
        for num in motion:
            #ある座り方のうちnum試行目
            csvpass = sys.argv[1] + "subject" + str(subject_index) + "/motion" + str(motion_index) + "/" + str(num) + "/JointAngle.csv"
            tmpdf = pd.read_csv(csvpass)
            df = pd.concat([df, tmpdf], axis = 1)

list_data = df.values.tolist()
print("距離行列計算中...")
for index in tqdm(range(len(list_data))):
    for col in range(8):
        M = np.reshape(list_data[index], (29, 8))[:,col].reshape(29,1)
        bc.Dis_Mat_list[col] += distance.cdist(M, M, metric='euclidean')

darray = distance.squareform(sum(bc.Dis_Mat_list))
Distance = sum(bc.Dis_Mat_list)
result = linkage(darray, method = "average")
# print(result)
df2 = pd.read_csv(sys.argv[1] + "1,3_2_result/Distance.csv", index_col=0)
dendrogram(result,labels=df2.columns)
plt.rcParams['font.size'] = 10 #フォントサイズを設定
plt.rcParams["font.family"] = "Times New Roman"
plt.title("Dendrogram")
# plt.show()
plt.show("./dendrogram_by_angle.png")
print("関節角を使った階層型クラスタリングが成功しました")
plt.cla
NUM_CLUSTERS_RANGE = range(2,29)
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

plt.savefig("/home/kei/document/experiments/method/1,3_2_result/シルエット係数.png")
