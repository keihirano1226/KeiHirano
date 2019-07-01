import pandas as pd
import numpy as np
from enum import Enum

#回転済みの座標値の読込
df = pd.read_csv('Rotated.csv')
#時間フレームの保存
dfTime = df.Time
dfall = dfTime
#座標フレームの保存
dfCoordinate = df.drop('Time', axis=1)
VectorMatrix = np.zeros((550,42))

#--------書き換えゾーン--------#

#関節のスタート位置(岡田さんのデータを扱う場合と，その他の場合で書き換えるべき)
#背筋、首、右鎖骨、右上腕、右前腕、左鎖骨、左上腕、左前腕、骨盤右、右大腿部、右すね、骨盤左、左大腿部、左すね
#関節開始位置の記述
JointStart = [14,0,0,1,3,0,2,5,14,7,9,14,8,11]
#関節終了位置の記述
JointEnd = [0,13,1,3,4,2,5,6,7,9,10,8,11,12]
#ベクトルの名前のリスト
#VectorList = [,,,,,,,,]

#--------書き換えゾーン--------#

"""
class Stick(Enum):
    spinal = 0
    Neck = 1
    ClavicleR = 2
    UpperarmR = 3
    ForearmR = 4
    ClavicleL = 5
    UpperarmL = 6
    ForearmL = 7
    PelvisR = 8
    FemurR = 9
    ShinR = 10
    PelvisL = 11
    FemurL = 12
    ShinL = 13
"""
StickMatrix = np.zeros((14,3))

for i in range(len(dfCoordinate)):
	df1 = dfCoordinate[i:i+1].values
	#1フレームの情報を一度15*3の行列に変換
	Frame = np.reshape(df1,(15,3))
	#各ベクトルの作成及び正規化
	for j in range(len(JointStart)):
		vector = Frame[JointEnd[j],:] - Frame[JointStart[j],:]
		vector1 = vector / np.linalg.norm(vector)
		StickMatrix[j,:] = vector1
	stickvector = np.reshape(StickMatrix,(1,42))
	VectorMatrix[i,:] = stickvector
PoseData = pd.DataFrame(VectorMatrix)
dfall = pd.concat([dfall,PoseData],axis = 1)
dfall.to_csv("NormarizedVector.csv", index= False)
