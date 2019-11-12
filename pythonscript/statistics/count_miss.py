import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csvpass = "/home/shoda/Documents/mitsu/3dbone.csv"
data = pd.read_csv(csvpass).iloc[:, list(range(1,76,3))].rename(columns=lambda s:s.rstrip("X")) #各関節の一つの座標値をとってくる
cnt_miss =data.isnull().sum()

csvpass2 = "/home/shoda/Documents/mitsu/proposed_idea/3dbone_fixed.csv"
data2 = pd.read_csv(csvpass2).iloc[:, list(range(1,76,3))].rename(columns=lambda s:s.rstrip("X")) #各関節の一つの座標値をとってくる
cnt_miss2 =data2.isnull().sum()

csvpass3 = "/home/shoda/Documents/3danalyze/3dbone_manual.csv"
data3 = pd.read_csv(csvpass3).iloc[:, list(range(1,76,3))].rename(columns=lambda s:s.rstrip("X")) #各関節の一つの座標値をとってくる
cnt_miss3 =data3.isnull().sum()

cnt = pd.concat([cnt_miss, cnt_miss2, cnt_miss3], axis=1, join='inner')
cnt.columns = ['origin', 'proposed', 'manual']

cnt.plot.bar(y=['origin', 'proposed', 'manual'], colormap='Accent')
plt.title('Number of missing value (per 200 frames)', size=16)
plt.subplots_adjust(left=0.1, right=0.95, bottom=0.2, top=0.9)
plt.savefig('pythonscript/statistics/missing_cnt.png')