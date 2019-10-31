import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csvpass = "/home/shoda/Documents/mitsu/3dbone.csv"
data = pd.read_csv(csvpass).iloc[:, list(range(1,76,3))].rename(columns=lambda s:s.rstrip("X")) #各関節の一つの座標値をとってくる
cnt_miss =data.isnull().sum()

csvpass2 = "/home/shoda/Documents/mitsu/proposed_idea/3dbone_fixed.csv"
data2 = pd.read_csv(csvpass2).iloc[:, list(range(1,76,3))].rename(columns=lambda s:s.rstrip("X")) #各関節の一つの座標値をとってくる
cnt_miss2 =data2.isnull().sum()

cnt = pd.concat([cnt_miss, cnt_miss2], axis=1, join='inner')
cnt.columns = ['origin', 'proposed']

cnt.plot.bar(y=['origin', 'proposed'])
plt.title('Number of missing value (per 200 frames)', size=16)
plt.subplots_adjust(left=0.1, right=0.95, bottom=0.2, top=0.9)
plt.savefig('pythonscript/statistics/missing_cnt.png')