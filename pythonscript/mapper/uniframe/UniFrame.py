import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

def spline3(x,y,point,deg):
    tck,u = interpolate.splprep([x,y],k=deg,s=0)
    u = np.linspace(0,1,num=point,endpoint=True)
    spline = interpolate.splev(u,tck)
    return spline[0],spline[1]

def dfSpline(dataFrame):


if __name__ == '__main__':
    csvpass = "/home/kei/document/experiments/ICTH2019/SY01/SY5.csv"
    df = pd.read_csv(csvpass)
    unidf = dfSpline(df, 1000)
    print(unidf)
