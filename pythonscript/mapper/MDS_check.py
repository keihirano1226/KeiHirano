import numpy as np
from sklearn import manifold
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys
import pandas as pd
from enum import Enum
from matplotlib.colors import Normalize # Normalizeをimport
from procrustes import Procrustes as pro
#2クラスタの場合の描画
class cluster2(Enum):
    r = 1
    b = 2
class Product(Enum):
    r = "chair"
    g = "sofa"
    b = "nursing bed"

class random_color(Enum):
    g = 1
    b = 2
    c = 3
    m = 4
    y = 5
basepass = sys.argv[1]
df = pd.read_csv(basepass + "Distance.csv",index_col = 0)
dflabel = pd.read_csv(basepass + "labels.csv")
Distance = df.values
d_data = []
b_data = []
for i in range(5):
    print(i)

    mds = manifold.MDS(n_components=2, dissimilarity="precomputed", random_state=i+1)
    pos = mds.fit_transform(Distance)
    """
    if i == 0:
        pos0 = pos
    else:
        [d,pos,t] = pro.procrustes(pos0,pos)
        d_data.append(d)
        b_data.append(t["scale"])
    """
    labels = df.index
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams['font.size'] = 20 #フォントサイズを設定


    for label, x, y in zip(labels, pos[:, 0], pos[:, 1]):
        plt.plot(x,y,color = random_color(i+1).name,marker = "o")
        plt.annotate(
            label,
            xy = (x, y), xytext = (20, -20),
            textcoords = 'offset points', ha = 'right', va = 'bottom'
        )
    plt.show()
    plt.cla()
"""
d_array = np.array(d_data).reshape(len(d_data),1)
b_array = np.array(b_data).reshape(len(b_data),1)
Data = np.concatenate([d_array,b_array],1)
df = pd.DataFrame(Data,columns = ["d","b"])
df.to_csv(sys.argv[1] + "simi.csv")
"""
