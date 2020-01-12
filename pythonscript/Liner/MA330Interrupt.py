import pandas as pd
import sys
df = pd.read_csv(sys.argv[1] + '3dboneRotated.csv')
#df = pd.read_csv(sys.argv[1] + 'output.csv')
df1 = df.replace(0.000, pd.np.nan)
df1 = df1.interpolate(limit_direction='both')
df1 = df1.round(3)
"""
#print(df1.Nosex)
#print(df1.Nosex.interpolate('spline', order=2))
for column_name, item in df1.iteritems():
    #print(column_name)
    print(item)
    item = item.interpolate('spline', order=2)
"""
print(df1)
df1.to_csv(sys.argv[1] + '3DFiltered.csv', index = 0)
