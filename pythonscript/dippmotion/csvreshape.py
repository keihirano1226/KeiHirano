import pandas as pd
import numpy as np

csvpass = "/home/kei/document/experiments/2019.06.06/backwalk/Yaxistest.csv"
df = pd.read_csv(csvpass)
imagevalue = df.values
print(imagevalue.shape[1])
imagevalue2 = np.reshape(imagevalue,(int(imagevalue.shape[1]/2), 2))
print(imagevalue2.shape)
print(type(imagevalue2))
df2 = pd.DataFrame(imagevalue2)
df2.to_csv("/home/kei/document/experiments/2019.06.06/backwalk/Yaxis2D.csv", header = 0,index = 0)
