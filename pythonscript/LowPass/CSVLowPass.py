import pandas as pd
import numpy as np
import sys
import glob

from scipy import signal
import matplotlib.pyplot as plt

InputFileName = sys.argv[1] + '2DInterrupt.csv'

df = pd.read_csv(InputFileName)
dfIndex = df.time
dfall = dfIndex
#dfTime = dfIndex /20
#print("hello")
dfCoordinate = df.drop('time', axis = 1)

t = dfIndex.values/30

def ColumnLowPass(y):
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
    filtered = signal.filtfilt(b1, a1, y)

    return filtered

for column_name, item in dfCoordinate.iteritems():
    #y = df.column_name.values
    #print(item)
    y = item.values
    #print(type(column_name))
    FilteredSignal = ColumnLowPass(y)
    #FilteredSignal = np.reshape(FilteredSignal1,(len(FilteredSignal1), 1))
    SignalFrame = pd.Series(data=FilteredSignal, name = column_name, dtype='float')
    #SignalFrame = SignalFrame.rename(columns=column_name)
    dfall = pd.concat([dfall,SignalFrame],axis = 1)
    #print(FilteredSignal)
dfall.to_csv(sys.argv[1] + "2DFiltered.csv", index = False)
