import pandas as pd
df = pd.read_csv('save2.csv',index_col = 0)
df1 = df.replace(0.000, pd.np.nan)
df1 = df1.replace('nan', pd.np.nan)
df1 = df1.interpolate('spline', order=2, limit_direction='both')
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
df1.to_csv('PoseSplineOut.csv')

