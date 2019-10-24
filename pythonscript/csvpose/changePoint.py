import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys

#ただ首y座標の時系列データをプロットするだけ
df = pd.read_csv(sys.argv[1] + '/output.csv')
df_neckx = df['Necky']
plt.figure()
df_neckx.plot()
plt.savefig('neckMotion.png')
print(df.info())