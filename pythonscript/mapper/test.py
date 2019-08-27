import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from procrustes import Procrustes
from uniframe import resampling

csvpass1 = "/home/kei/document/experiments/ICTH2019/SY/SY2.csv"
csvpass2 = "/home/kei/document/experiments/ICTH2019/SK/SK1.csv"
df1 = pd.read_csv(csvpass1)
df2 = pd.read_csv(csvpass2)
uni_df1 = resampling.dfSpline(df1, 1000)
uni_df2 = resampling.dfSpline(df2, 1000)
uni_df1.to_csv("/home/kei/document/experiments/ICTH2019/SY/UniSY2.csv",index = 0)
uni_df2.to_csv("/home/kei/document/experiments/ICTH2019/SK/UniSK1.csv",index = 0)
df1 = pd.read_csv("/home/kei/document/experiments/ICTH2019/SY/UniSY2.csv",index_col = 0)
df2 = pd.read_csv("/home/kei/document/experiments/ICTH2019/SK/UniSK1.csv",index_col = 0)
df1_Mat = df1.values
df2_Mat = df2.values
[d, Z, t] = Procrustes.procrustes(df1_Mat, df2_Mat)
#print(Z.shape)
rotated_df2 = pd.DataFrame(data = Z, columns = df1.columns)
rotated_df2.to_csv("/home/kei/document/experiments/ICTH2019/SY/Rotated2SK1SY1.csv",index = 0)
