import pandas as pd
import numpy as np
import sys
import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
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
result = linkage(darray, method = "average")
# print(result)
df2 = pd.read_csv(sys.argv[1] + "1,3_result/Distance.csv", index_col=0)
dendrogram(result,labels=df2.columns)
plt.rcParams['font.size'] = 10 #フォントサイズを設定
plt.rcParams["font.family"] = "Times New Roman"
plt.title("Dendrogram")
# plt.show()
plt.show("./dendrogram_by_angle.png")
print("関節角を使った階層型クラスタリングが成功しました")
