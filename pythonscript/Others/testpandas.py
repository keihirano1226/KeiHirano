import pandas as pd
import itertools
df = pd.read_csv('output.csv', index_col = 0)
df1 = df[0:1]
#df1 = df
print(type(df1))
df2 = df1.values.tolist()
#df2 = itertools.chain(*df2)
df2 = list(df2)
print(type(df2))
print(len(df2))
#print(df2.shape)
print(df2)
