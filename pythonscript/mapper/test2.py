import pandas as pd
import numpy as np
from minepy import MINE

df1 = pd.read_csv("/home/kei/document/experiments/ICTH2019/SY/UniSY2.csv")
df2 = pd.read_csv("/home/kei/document/experiments/ICTH2019/SK/UniSK1.csv")
#columns = ["LSholderX","LSholderY","LSholderZ"]
columns = ["LSholderX"]
X = df1[columns].values.tolist()
Y = df2[columns].values.tolist()
mine = MINE()
print(X.shape)
mine.compute_score(X,Y)
print(mine.mic())
