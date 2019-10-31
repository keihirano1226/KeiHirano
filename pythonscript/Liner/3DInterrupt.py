import pandas as pd
import sys

isFixed = 1 #アフィン変換されているか否か

if isFixed: 
    df = pd.read_csv(sys.argv[1] + '3dbone_fixed.csv')
else:
    df = pd.read_csv(sys.argv[1] + '3dbone.csv')
    
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
if isFixed: 
    df1.to_csv(sys.argv[1] + '3DInterrupt_fixed.csv', index = 0)
else:
    df1.to_csv(sys.argv[1] + '3DInterrupt.csv', index = 0)
    
