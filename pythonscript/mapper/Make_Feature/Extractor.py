import pandas as pd
import numpy as np

def Feature(matrix, method):
    Feature_vector = []
    vector_column = []
    OpenPosecolumns = matrix.columns
    method_name = ["ave","dev","max_time"]
    """本番用
    OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","RWrist","LWrist","MidHip",\
    "RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
    Coordinate2 = ["X","Y","Z"]
    for point in OpenPoseJoint:
        for coordinate in Coordinate2:
            newcolumn = point + coordinate
            OpenPosecolumns.append(newcolumn)
    selectedparts = body[OpenPosecolumns]
    OpenPoseJoint = ["Neck","LSholder","RElbow","LElbow","LWrist","MidHip",\
    "RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
    Coordinate2 = ["X","Y","Z"]
    method_name = ["ave","dev","max_time"]
    for point in OpenPoseJoint:
        for coordinate in Coordinate2:
            newcolumn = point + coordinate
            OpenPosecolumns.append(newcolumn)
    selectedparts = matrix[OpenPosecolumns]
    """
    if method[0] == 1:
        for data in OpenPosecolumns:
            newcolumn = data + "_" + method_name[0]
            vector_column.append(newcolumn)
        vector = matrix.mean()
        vector.index = vector_column
    if method[1] == 1 and method[0] == 1:
        vector_column = []
        for data in OpenPosecolumns:
            newcolumn = data + "_" + method_name[1]
            vector_column.append(newcolumn)
        vector1 = matrix.var(ddof=False)
        vector1.index = vector_column
        vector = pd.concat([vector,vector1])
    elif method[1] == 1 and method[0] == 0:
        vector_column = []
        for data in OpenPosecolumns:
            newcolumn = data + "_" + method_name[1]
            vector_column.append(newcolumn)
        vector = matrix.var(ddof=False)
        vector.index = vector_column
    if method[2] == 1 and method[0] == 0 and method[1] == 0 :
        print("hello")
        vector_column = []
        for data in OpenPosecolumns:
            newcolumn = data + "_" + method_name[2]
            vector_column.append(newcolumn)
        vector = matrix.idxmax() / len(selectedparts)
        vector.index = vector_column
    elif method[2] == 1 and (method[0] == 1 or method[1] == 1):
        vector_column = []
        for data in OpenPosecolumns:
            newcolumn = data + "_" + method_name[2]
            vector_column.append(newcolumn)
        vector2 = selectedparts.idxmax() / len(selectedparts)
        vector2.index = vector_column
        vector = pd.concat([vector,vector2])
    vectorF = vector.transpose()
    return vectorF

if __name__ == '__main__':
    csvpass = "/home/kei/document/experiments/ICTH2019/SY01/SY5.csv"
    df = pd.read_csv(csvpass)
    message = Feature(df,[1,1,1])
    message.to_csv("/home/kei/document/experiments/ICTH2019/SY01/Feature5.csv")
