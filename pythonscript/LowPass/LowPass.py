import pandas as pd
import numpy as np
import sys
import glob

from scipy import signal
import matplotlib.pyplot as plt

InputFileName = sys.argv[1] + 'SplineOut.csv'

df = pd.read_csv(InputFileName)
dfIndex = df.time
#dfTime = dfIndex /20
#print("hello")
dfCoordinate = df.drop('time', axis = 1)

t1 = dfIndex.values/30
t = t1

y1 = df.Neckx.values
y2 = df.Necky.values



"""
t = tuple(t2)
y1 = tuple(y11)
y2 = tuple(y21)
"""

# パラメータ設定
dt = 1/30
fn = 1/(2*dt)

fp = 1                     # 通過域端周波数[Hz]
fs = 10                         # 阻止域端周波数[Hz]
gpass = 1                       # 通過域最大損失量[dB]
gstop = 40                      # 阻止域最小減衰量[dB]
# 正規化
Wp = fp/fn
Ws = fs/fn

# バターワースフィルタ
N, Wn = signal.buttord(Wp, Ws, gpass, gstop)

b1, a1 = signal.butter(N, Wn, "low")
print(type(y1))
y1filtered = signal.filtfilt(b1, a1, y1)
print("hello")
y2filtered = signal.filtfilt(b1, a1, y2)





#プロット
plt.figure()
plt.plot(t, y1, "b")
plt.plot(t, y2, "r")
plt.plot(t, y1filtered, "r", linewidth=2, label="y1filtered")
plt.plot(t, y2filtered, "r", linewidth=2, label="y2filtered")
plt.xlim(0, 4)
plt.legend(loc="upper right")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
