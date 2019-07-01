import pandas as pd
import numpy as np
from scipy.optimize import minimize

pi = np.pi
#3軸回転の関節用
def rot3M(p):
    # 回転行列を計算する
    px = p[0]
    py = p[1]
    pz = p[2]

    # 物体座標系の 1->2->3 軸で回転させる
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(px), np.sin(px)],
                   [0, -np.sin(px), np.cos(px)]])
    Ry = np.array([[np.cos(py), 0, -np.sin(py)],
                   [0, 1, 0],
                   [np.sin(py), 0, np.cos(py)]])
    Rz = np.array([[np.cos(pz), np.sin(pz), 0],
                   [-np.sin(pz), np.cos(pz), 0],
                   [0, 0, 1]])
    R = Rz.dot(Ry).dot(Rx)

    # 物体座標系の 3->2->1 軸で回転させる
    #Rx = np.array([[1, 0, 0],
    #                [0, np.cos(px), np.sin(px)],
    #                [0, -np.sin(px), np.cos(px)]])
    #Ry = np.array([[np.cos(py), 0, -np.sin(py)],
    #                [0, 1, 0],
    #                [np.sin(py), 0, np.cos(py)]])
    #Rz = np.array([[np.cos(pz), np.sin(pz), 0],
    #                [-np.sin(pz), np.cos(pz), 0],
    #                [0, 0, 1]])
    #R = Rx.dot(Ry).dot(Rz)

    # 空間座標系の 1->2->3 軸で回転させる
    # Rx = np.array([[1, 0, 0],
    #                [0, np.cos(px), -np.sin(px)],
    #                [0, np.sin(px), np.cos(px)]])
    # Ry = np.array([[np.cos(py), 0, -np.sin(py)],
    #                [0, 1, 0],
    #                [np.sin(py), 0, np.cos(py)]])
    # Rz = np.array([[np.cos(pz), np.sin(pz), 0],
    #                [-np.sin(pz), np.cos(pz), 0],
    #                [0, 0, 1]])
    # R = Rx.dot(Ry).dot(Rz)

    # 空間座標系の 3->2->1 軸で回転させる
    # Rx = np.array([[1, 0, 0],
    #                [0, np.cos(px), -np.sin(px)],
    #                [0, np.sin(px), np.cos(px)]])
    # Ry = np.array([[np.cos(py), 0, -np.sin(py)],
    #                [0, 1, 0],
    #                [np.sin(py), 0, np.cos(py)]])
    # Rz = np.array([[np.cos(pz), np.sin(pz), 0],
    #                [-np.sin(pz), np.cos(pz), 0],
    #                [0, 0, 1]])
    # R = Rz.dot(Ry).dot(Rx)
    return R

#1軸回転行列の定義
def rot1M(p4):
    p1x = p4
    R1 = np.array([[1, 0, 0],
                   [0, np.cos(p1x), np.sin(p1x)],
                   [0, -np.sin(p1x), np.cos(p1x)]])
    return R1


#足の関節角の計算
df = pd.read_csv('NormarizedVector.csv')
#時間フレームの保存
dfTime = df.Time
dfall = dfTime
#全ベクトルフレームの保存
dfVector = df.drop('Time', axis=1)
Vector = dfVector.values
FemurR = Vector[:,27:30]
ShinR = Vector[:,30:33]
UpperarmR = Vector[:,9:12]
ForearmR = Vector[:,12:15]
FemurL = Vector[:,36:39]
ShinL = Vector[:,39:42]
UpperarmL = Vector[:,18:21]
ForearmL = Vector[:,21:24]


#右膝及び右足首座標値の計算及び座標値行列の作成
KneeR = FemurR
AnkleR = FemurR + ShinR
KneeL = FemurL
AnkleL = FemurL + ShinL
ElbowR = UpperarmR
WristR = ElbowR + ForearmR
ElbowL = UpperarmL
WristL = ElbowR + ForearmR

PositionMatrix = np.concatenate([KneeR, AnkleR,KneeL,AnkleL,ElbowR,WristR,ElbowL,WristL],axis = 1)
FemurRVec = np.array([0,-1,0]).T
ShinRVec = np.array([0,-1,0]).T
FemurLVec = np.array([0,-1,0]).T
ShinLVec = np.array([0,-1,0]).T
UpperarmRVec = np.array([0,-1,0]).T
ForearmRVec = np.array([0,-1,0]).T
UpperarmLVec = np.array([0,-1,0]).T
ForearmLVec = np.array([0,-1,0]).T

JointAngleMatrix = np.zeros((PositionMatrix.shape[0],8))

#--------剛体2リンクベクトルの座標値を返す関数------------
def func(x):
    #親ベクトルの回転行列計算用の数値読み込み
    p = x[0:3]
    R1 = rot3M(p)
    #子ベクトルの回転行列計算用の数値読み込み
    p4 = x[3]
    R2 = rot1M(p4)

    #それぞれの座標値を計算
    EstimatedVector1 = np.dot(R1, FemurRVec)
    RChild = np.dot(R1,R2)
    EstimatedVector2 = EstimatedVector1 + np.dot(RChild, ShinRVec)

    return EstimatedVector1, EstimatedVector2
#---------ここまで---------------------------------


for i in range(int(PositionMatrix.shape[0])):
    KneeRPosition = PositionMatrix[i:i+1,0:3]
    AnkleRPosition = PositionMatrix[i:i+1,3:6]
    KneeLPosition = PositionMatrix[i:i+1,6:9]
    AnkleLPosition = PositionMatrix[i:i+1,9:12]
    ElbowRPosition = PositionMatrix[i:i+1,12:15]
    WristRPosition = PositionMatrix[i:i+1,15:18]
    ElbowLPosition = PositionMatrix[i:i+1,18:21]
    WristLPosition = PositionMatrix[i:i+1,21:24]


#-------各種目的関数の定義------------------------

    #右足用目的関数の定義
    def ObjectiveFuncLegR(x):
        EstimatedVector1, EstimatedVector2 = func(x)

        return np.linalg.norm(KneeRPosition - EstimatedVector1) + np.linalg.norm(AnkleRPosition - EstimatedVector2)
    #左足用目的関数の定義
    def ObjectiveFuncLegL(x):
        EstimatedVector3, EstimatedVector4 = func(x)

        return np.linalg.norm(KneeLPosition - EstimatedVector3) + np.linalg.norm(AnkleLPosition - EstimatedVector4)

"""
#--------腕関節節角度計算用なので，今回は使わず--------#
    #右腕用目的関数の定義
    def ObjectiveFuncArmR(x):
        EstimatedVector5, EstimatedVector6 = func(x)

        return np.linalg.norm(ElbowRPosition - EstimatedVector5) + np.linalg.norm(WristRPosition - EstimatedVector6)

    #左腕用目的関数の定義
    def ObjectiveFuncArmL(x):
        EstimatedVector7, EstimatedVector8 = func(x)

        return np.linalg.norm(ElbowLPosition - EstimatedVector7) + np.linalg.norm(WristLPosition - EstimatedVector8)

#--------足関節角度計算用なので，今回は使わず--------#
"""
    #初期解: (0,0)
    x0 = np.array([0,0,0,0],dtype=float)

    #範囲制約(腕と足で関節可動域が異なるため)
    bnds = ((-pi,pi),(-pi/2,pi/2),(-pi/2,pi/2),(-pi,0))
    bnds1 = ((-pi,pi),(-pi/2,pi/2),(-pi/2,pi/2),(0,pi))

    #最適化
    res0 = minimize(ObjectiveFuncLegR, x0, method='SLSQP', bounds = bnds)
    res1 = minimize(ObjectiveFuncLegL, x0, method='SLSQP', bounds = bnds)
    #res2 = minimize(ObjectiveFuncArmR, x0, method='SLSQP', bounds = bnds1)
    #res3 = minimize(ObjectiveFuncArmL, x0, method='SLSQP', bounds = bnds1)
    #print(type(res["x"]))
    #print(res["x"])
    #JointAngleMatrix[i,:] = np.concatenate([res0["x"],res1["x"],res2["x"],res3["x"]],axis=0)
    res0["x"][1] = -res0["x"][1]
    res0["x"][3] = -res0["x"][3]
    res1["x"][3] = -res1["x"][3]
    JointAngleMatrix[i,:] = np.concatenate([res0["x"],res1["x"]],axis=0)
JointAngleMatrix = JointAngleMatrix*180/pi
JointAngleData = pd.DataFrame(JointAngleMatrix)
dfall = pd.concat([dfall,JointAngleData],axis = 1)
dfall.to_csv("LegJointAngleData.csv", index= False)
