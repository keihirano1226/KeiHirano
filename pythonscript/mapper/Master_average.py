#全身平均モーションを作成するようのスクリプト
import pandas as pd
import numpy as np
from BodyColumn import All_joint as AJ
basepass = "/home/kei/document/experiments/Master2/"
posebasepass = basepass + "Unified/"

OpenPoseJoint,bodycolumns,Dis_Mat_list = AJ.Member(13)
dfpose = pd.read_csv(posebasepass + "no33_1.csv")
dfpose = dfpose[bodycolumns]
AveragePoseData = np.zeros((len(dfpose),len(dfpose.columns)))
AveragePose1 = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
AveragePose2 = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
i = 0
"""
for member in class1:
    dfpose = pd.read_csv(basepass + member + ".csv")
    dfpose = dfpose[bodycolumns]
    AveragePose1 += dfpose
    i+=1

AveragePose1 = AveragePose1 / i
i = 0
AveragePose1.to_csv(basepass + "/AveragePose2.1.1.csv")
for member in class2:
    dfpose = pd.read_csv(basepass + member + ".csv")
    dfpose = dfpose[bodycolumns]
    AveragePose2 += dfpose
    i+=1

AveragePose2 = AveragePose2 / i
AveragePose2.to_csv(basepass + "/AveragePose2.1.2.csv")
"""
i1=0
i2=0
dflabel = pd.read_csv(basepass + "AJ_result/labels.csv")
for index, row in dflabel.iterrows():
    """
    print(row["ID"])
    print(row["class2"])
    """
    if row["class2"] == 2:
        dfpose = pd.read_csv(posebasepass + row["ID"] + ".csv")
        dfpose = dfpose[bodycolumns]
        AveragePose2 += dfpose
        i2+=1
    if row["class2"] == 1:
        dfpose = pd.read_csv(posebasepass + row["ID"] + ".csv")
        dfpose = dfpose[bodycolumns]
        AveragePose1 += dfpose
        i1+=1
AveragePose1 = AveragePose1 / i1
AveragePose2 = AveragePose2 / i2
AveragePose1.to_csv(basepass + "/AveragePose1.csv")
AveragePose2.to_csv(basepass + "/AveragePose2.csv")
