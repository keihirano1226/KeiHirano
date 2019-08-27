import pandas as pd
import numpy as np
import mca
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA #主成分分析器
csvpass = "/home/kei/document/experiments/ICTH2019/result_ave/ave_FeatureMatrix.csv"
df = pd.read_csv(csvpass, index_col=0, header = 0)
ncol = df.shape[1]
#df = df.dropna(inplace=True)
#print(df)
dfs = df.iloc[:, 1:].apply(lambda x: (x-x.mean())/x.std(), axis=0)
pca = PCA()
feature = pca.fit(dfs)
feature = pca.transform(dfs)
plt.scatter(feature[:, 0], feature[:, 1], c='b',marker='o')
labels = df.index
for label,x,y in zip(labels,feature[:,0],feature[:,1]):
    plt.annotate(label,xy = (x, y))
plt.grid()
plt.xlabel("PC1")
plt.ylabel("PC2")
dfindex2 = pd.DataFrame(pca.components_, columns=df.columns[1:], index=["PC{}".format(x + 1) for x in range(9)])
pcindex = pd.DataFrame(feature, columns=["PC{}".format(x + 1) for x in range(9)]).head()
dfindex = pd.DataFrame(pca.explained_variance_ratio_, index=["PC{}".format(x + 1) for x in range(9)])
dfindex.to_csv("/home/kei/document/experiments/ICTH2019/result_ave/ave_寄与率.csv")
pcindex.to_csv("/home/kei/document/experiments/ICTH2019/result_ave/ave_主成分得点.csv")
dfindex2.to_csv("/home/kei/document/experiments/ICTH2019/result_ave/ave_固有ベクトル.csv")

"""
map_data = mca.MCA(df, ncols = ncol)
rows = map_data.fs_r(N=2)
cols = map_data.fs_c(N=2)
#print(df)
plt.scatter(rows[:,0], rows[:,1], c='b',marker='o')
labels = df.index
for label,x,y in zip(labels,rows[:,0],rows[:,1]):
    plt.annotate(label,xy = (x, y))

plt.scatter(cols[:,0], cols[:,1], c='r',marker='x')
labels = df.columns
for label,x,y in zip(labels,cols[:,0],cols[:,1]):
    plt.annotate(label,xy = (x, y))
"""

plt.savefig("/home/kei/document/experiments/ICTH2019/result_ave/ave_pca_map.png")
