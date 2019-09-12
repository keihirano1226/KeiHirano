import numpy as np
import pandas as pd
import Kalman
import sys

csvpass = sys.argv[1] + "3DInterrupt2.csv"
df = pd.read_csv(csvpass)
df2 = df.Frame.values
df2 = np.reshape(df2, (len(df2), 1))
print(df2.shape)
for column_name, item in df.iteritems():
    if column_name != "Frame":
        FilteredX = Kalman.forward(item, 0.01, 0.01, 0.1)
        s = pd.Series(FilteredX)
        sn = s.values
        sn = np.reshape(sn, (len(sn), 1))
        df2 = np.concatenate([df2, sn], 1)
#X = df.RSholderX.values
#FilteredX = forward(X, 0.008, 0.008, 4)
#print(type(FilteredX))
#s = pd.Series(FilteredX)
dfall = pd.DataFrame(data = df2, columns = df.columns)
dfall.to_csv(sys.argv[1] + "3DFiltered.csv",index = 0)
