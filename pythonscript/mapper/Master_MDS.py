import numpy as np
from sklearn import manifold
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import pandas as pd
from enum import Enum
from matplotlib.colors import Normalize # Normalizeをimport
#2クラスタの場合の描画
class cluster2(Enum):
    r = 1
    b = 2
class Product(Enum):
    r = "chair"
    g = "sofa"
    b = "nursing bed"
basepass = sys.argv[1]
df = pd.read_csv(basepass + "Distance.csv",index_col = 0)
dflabel = pd.read_csv(basepass + "labels.csv")
Distance = df.values
mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(Distance)
labels = df.index
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = 20 #フォントサイズを設定
#plt.scatter(pos[:, 0], pos[:, 1], marker = 'o')
#plt.text(-1500,-1000, "chair\nnursing bed\nsofa", size = 20, color = "k",verticalalignment='bottom')
x_cluster1 = []#sofa or 1
y_cluster1 = []#sofa or 1
x_cluster2 = []#chair or 2
y_cluster2 = []#chair or 2
x_cluster3 = []#nursing bed
y_cluster3 = []#nursing bed
"""
#クラスタ数が3つの時に使う
for x,y,ID in zip(pos[:,0],pos[:,1],dflabel["product"]):
    if ID == "sofa":
        x_cluster1.append(x)
        y_cluster1.append(y)
    elif ID == "chair":
        x_cluster2.append(x)
        y_cluster2.append(y)
    elif ID == "nursing bed":
        x_cluster3.append(x)
        y_cluster3.append(y)
plt.scatter(x_cluster1,y_cluster1,color = "r",marker = "o", label='sofa')
plt.scatter(x_cluster2,y_cluster2,color = "g",marker = "o", label='chair')
plt.scatter(x_cluster3,y_cluster3,color = "b",marker = "o", label='nursing bed')
#クラスタ数が3つの時に使う
#クラスタ数が2つの時に使う
for x,y,ID in zip(pos[:,0],pos[:,1],dflabel["class2"]):
    if ID == 1:
        x_cluster1.append(x)
        y_cluster1.append(y)
    elif ID == 2:
        x_cluster2.append(x)
        y_cluster2.append(y)
plt.scatter(x_cluster1,y_cluster1,color = "r",marker = "o", label='cluster1')
plt.scatter(x_cluster2,y_cluster2,color = "b",marker = "o", label='cluster2')
#クラスタ数が2つの時に使う
plt.legend(loc = "lower left")
"""
#MMSE_score = dflabel["MMSE"].values
im = plt.scatter(pos[:,0],pos[:,1],c = dflabel.BI,cmap='coolwarm', norm=Normalize(vmin=0, vmax=100),marker = "o")
#plt.plot(x,y,color = Product(ID).name,marker = "o")
for label, x, y, ID in zip(labels, pos[:, 0], pos[:, 1],dflabel["MMSE"]):
    #plt.plot(x,y,color = [0.0,float(ID/30),0.0],cmap=cm.Accent,marker = "o")
    plt.annotate(
        label,
        xy = (x, y), xytext = (20, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom'
    )
#ax.text(0.2, 0.2, "Chair", size = 20, color = "blue")
plt.colorbar(im)
plt.show()
