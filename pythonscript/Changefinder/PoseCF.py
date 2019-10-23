import matplotlib.pyplot as plt
import changefinder
import numpy as np
import sys
import pandas as pd
"""
data=np.concatenate([np.random.normal(0.7, 0.05, 300),
np.random.normal(1.5, 0.05, 300),
np.random.normal(0.6, 0.05, 300),
np.random.normal(1.3, 0.05, 300)])
"""
csvpass = sys.argv[1] + "3DFiltered.csv"
df = pd.read_csv(csvpass)

data = df.LSholderX.diff()
data2 = data.drop(data.index[[0]])
"""
data = df.LSholderX.values
"""
print(data)
cf = changefinder.ChangeFinder(r=0.2, order=1, smooth=5)

ret = []
for i in data2:
    score = cf.update(i)
    ret.append(score)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(ret)
ax2 = ax.twinx()
ax2.plot(data,'r')
plt.show()
print(ret)
