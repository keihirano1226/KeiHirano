import pandas as pd
import numpy as np

df = pd.read_csv('NormarizedVector.csv')
#時間フレームの保存
dfTime = df.Time
dfall = dfTime
#ベクトルフレームの保存
dfCoordinate = df.drop('Time', axis=1)
#ベクトル座標値の塊
Vector = dfCoordinate.values
#それぞれのスティックベクトルの取得
Spinal = Vector[:,0:3]
Neck = Vector[:,3:6]
ClavicleR = Vector[:,6:9]
UpperarmR = Vector[:,9:12]
ForearmR = Vector[:,12:15]
ClavicleL = Vector[:,15:18]
UpperarmL = Vector[:,18:21]
ForearmL = Vector[:,21:24]
PelvisR = Vector[:,24:27]
FemurR = Vector[:,27:30]
ShinR = Vector[:,30:33]
PelvisL = Vector[:,33:36]
FemurL = Vector[:,36:39]
ShinL = Vector[:,39:42]

#各種座標値の作成
Head = Spinal + Neck
Sternum = Spinal
ShoulderR = Sternum + ClavicleR
ElbowR = ShoulderR + UpperarmR
HandR = ElbowR + ForearmR
ShoulderL = Sternum + ClavicleL
ElbowL = ShoulderL + UpperarmL
HandL = ElbowL + ForearmL
KneeR = PelvisR + FemurR
AnkleR = KneeR + ShinR
KneeL = PelvisL + FemurL
AnkleL = KneeL + ShinL
Root = np.zeros(Spinal.shape)
PositionMatrix = np.concatenate([Head, Sternum, ShoulderR,ElbowR,HandR,ShoulderL,ElbowL,HandL,PelvisR,KneeR,AnkleR,PelvisL,KneeL,AnkleL,Root],axis = 1)
PositionData = pd.DataFrame(PositionMatrix)
dfall = pd.concat([dfall,PositionData],axis = 1)
dfall.to_csv('NormarizedPosition.csv', index = False)
#print(PositionMatrix)
#print(Spinal)
