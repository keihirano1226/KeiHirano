import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys


basepass = sys.argv[1]
df = pd.read_csv(basepass + "3DFiltered.csv")
X = df.Frame / 30
Y = df.RSholderZ
Y1 = Y.diff()
plt.rcParams['figure.figsize'] = [6.4, 4.8]
plt.rcParams["font.size"] = 20
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams["xtick.direction"] = "in"               #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams["ytick.direction"] = "in"               #y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
"""
plt.xlabel('time')
plt.ylabel("score")
plt.xlim(0,max(x))
plots = plt.plot(x, A)
plt.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
plt.savefig(basepass + "start_change" + str(w1*3) + ".png", bbox_inches='tight', pad_inches=0.1)
plt.cla()
"""
fig,ax1 = plt.subplots()
ax1.plot(X,Y,c = "r",label="pz")
ax2 = ax1.twinx()
ax2.plot(X,Y1,c = "b",label="vz")
plt.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1+h2, l1+l2, loc='lower right')
plt.xlim(0,max(X))
ax1.set_xlabel("t[s]")
ax1.set_ylabel("Z coordinate [m]")
ax2.set_ylabel("Vz [m/s]")
plt.show()
