import pandas as pd
import numpy as np
import math
import sys

def Dimention3(dataframe, method):
    CoordinateMatrix = dataframe.values
    polarMatrix = np.zeros([dataframe.shape[0],int(dataframe.shape[1]*2/3)])
    t = int(CoordinateMatrix.shape[1])/3
    for i in range(len(dataframe)):
        df1 = dataframe[i:i+1].values
        for j in range(int(CoordinateMatrix.shape[1]/3)):
            x = df1[0,3*j+0]
            y = df1[0,3*j+1]
            z = df1[0,3*j+2]
            if (x == 0 and y == 0 and z == 0):
                polarMatrix[i:i+1,2*j:2*j+1] = 0
                polarMatrix[i:i+1,2*j+1:2*j+2] = 0
                #polarMatrix[i:i+1,3*j+2:3*j+3] = 0
            else:
                theta = math.degrees(math.acos(z / math.sqrt(x*x + y*y + z*z)))
                phi = math.degrees(math.acos(x / math.sqrt(x*x + y*y)))
                r = math.sqrt(x*x + y*y + z*z)
                polarMatrix[i:i+1,2*j:2*j+1] = theta
                polarMatrix[i:i+1,2*j+1:2*j+2] = phi
                #polarMatrix[i:i+1,3*j+2:3*j+3] = phi

def DimentionUni(dataframe, height):
    CoordinateMatrix = dataframe.values
    polarMatrix = np.zeros([dataframe.shape[0],int(dataframe.shape[1])])
    t = int(CoordinateMatrix.shape[1])/3
    for i in range(len(dataframe)):
        df1 = dataframe[i:i+1].values
        for j in range(int(CoordinateMatrix.shape[1]/3)):
            x = df1[0,3*j+0]
            y = df1[0,3*j+1]
            z = df1[0,3*j+2]
            if (x == 0 and y == 0 and z == 0):
                polarMatrix[i:i+1,3*j:3*j+1] = x / height
                polarMatrix[i:i+1,3*j+1:3*j+2] = y / height
                polarMatrix[i:i+1,3*j+2:3*j+3] = z / height
            else:
                theta = math.degrees(math.acos(z / math.sqrt(x*x + y*y + z*z)))
                phi = math.degrees(math.acos(x / math.sqrt(x*x + y*y)))
                r = math.sqrt(x*x + y*y + z*z)
                polarMatrix[i:i+1,3*j:3*j+1] = x / height
                polarMatrix[i:i+1,3*j+1:3*j+2] = y / height
                polarMatrix[i:i+1,3*j+2:3*j+3] = z / height


    return polarMatrix
if __name__ == '__main__':
    csvpass = "/home/kei/document/experiments/ICTH2019/SY/SY5test.csv"
    df = pd.read_csv(csvpass)
    print(df)
    #dfdata = df.drop("Unnamed: 0",axis = 0)
    print(df.shape[1])
    polardata = Dimention3(df,1)
    df2 = pd.DataFrame(polardata,columns = df.columns)
    """
    message = Feature(df)
    message.to_csv("/home/kei/document/experiments/ICTH2019/SY01/SY5.csv")
    """
    df2.to_csv("/home/kei/document/experiments/ICTH2019/polar.csv")
    print(df2)
