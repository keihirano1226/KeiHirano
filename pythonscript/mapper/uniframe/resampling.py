import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

def spline3(x,y,point,deg):
    tck,u = interpolate.splprep([x,y],k=deg,s=0)
    u = np.linspace(0,1,num=point,endpoint=True)
    spline = interpolate.splev(u,tck)
    return spline[0],spline[1]

# データフレームをn=fへリサンプリング
def dfSpline(dataFrame, f):
    output = pd.DataFrame(data=list(range(f)))
    time = []
    for i in range(len(dataFrame)):
        time.append(i)
    for column_name, item in dataFrame.iteritems():
        if(column_name == 'Unnamed: 0'):
            continue
        index_new, item_ = spline3(time,item.tolist(),f,3)
        output[column_name] = item_

    return output
if __name__ == '__main__':
    basepass = "/home/kei/document/experiments/Hamano/H3_1/3DFiltered2.csv"
    df = pd.read_csv(basepass)
    unidf = dfSpline(df, 500)
    print(unidf)
    unidf.to_csv("H3_1.csv",index = 0)
