#全身平均モーションを作成するようのスクリプト
import pandas as pd
import numpy as np
from BodyColumn import All_joint as AJ
basepass = "/home/kei/document/experiments/Master/Unified/"
class1 = ["no33_1","no32_2"]
class2 = ["no33_2","no31_1","no9_2","no9_1","no32_1"]
OpenPoseJoint,bodycolumns,Dis_Mat_list = AJ.Member(7)
dfpose = pd.read_csv(basepass + "no33_1.csv")
dfpose = dfpose[bodycolumns]
AveragePoseData = np.zeros((len(dfpose),len(dfpose.columns)))
AveragePose1 = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
AveragePose2 = pd.DataFrame(data= AveragePoseData, columns = bodycolumns )
i = 0
for member in class1:
    dfpose = pd.read_csv(basepass + member + ".csv")
    dfpose = dfpose[bodycolumns]
    AveragePose1 += dfpose
    i+=1

AveragePose1 = AveragePose1 / i
i = 0
AveragePose1.to_csv(basepass + "/AveragePose1.1.csv")
for member in class2:
    dfpose = pd.read_csv(basepass + member + ".csv")
    dfpose = dfpose[bodycolumns]
    AveragePose2 += dfpose
    i+=1

AveragePose2 = AveragePose2 / i
AveragePose2.to_csv(basepass + "/AveragePose2.1.csv")
