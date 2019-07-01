import pandas as pd
import numpy as np
df = pd.read_csv('BodyRotated.csv')
#時間フレームの保存
dfTime = df.Time
dfall = dfTime
#座標フレームの保存
dfCoordinate = df.drop('Time', axis=1)
PoseMatrix = np.zeros(dfCoordinate.shape)
#腰関節の回転行列の保存用の定義
PelvisRotationMatrix = np.zeros((dfCoordinate.shape[0],9))

for i in range(len(dfCoordinate)):
	df1 = dfCoordinate[i:i+1].values
	#1フレームの情報を一度15*3の行列に変換
	Frame = np.reshape(df1,(15,3))
	#右肩の取得
	ShoulderR = Frame[1,:]
	#左肩の取得
	ShoulderL = Frame[2,:]
	#x軸の作成
	PelvisVector = ShoulderL - ShoulderR
	Xaxis = PelvisVector/ np.linalg.norm(PelvisVector)
	#Xaxis = np.reshape(Xaxis,(3,1))
	#胸部の取得
	Sternum = Frame[0,:]
	#腰中央
	PelvisCenter = Frame[14,:]
	#仮のy軸の作成
	SternumVector = Sternum - PelvisCenter
	TentativeYaxis = SternumVector / np.linalg.norm(SternumVector)

	#外積によるz軸の作成
	ZVector = np.cross(Xaxis, TentativeYaxis)
	Zaxis = ZVector / np.linalg.norm(ZVector)

	#外積による真のy軸の再定義
	YVector = np.cross(Zaxis, Xaxis)
	Yaxis = YVector / np.linalg.norm(YVector)

	#姿勢変換行列Rの作成
	#print(Zaxis.shape)
	Rvector = np.r_[Xaxis,Yaxis,Zaxis]
	R = np.reshape(Rvector,(3, 3))
	PelvisRotationMatrix[i,:9] = Rvector
	#R = np.matrix(Xaxis,Yaxis,Zaxis)
	#姿勢変換された座標値の作成
	Pose = np.dot(R, Frame.T)
	Pose = Pose.T
	Pose = np.reshape(Pose,(1,45))
	PoseMatrix[i,:45] = Pose
PoseData = pd.DataFrame(PoseMatrix)
columns = ['R11','R12','R13','R21','R22','R23','R31','R32','R33']
RotationMatrixData = pd.DataFrame(data = PelvisRotationMatrix, columns = columns,dtype='float')
dfall = pd.concat([dfall,PoseData],axis = 1)
dfall.to_csv("ArmRotated.csv", index = False)
dfRotation = pd.concat([dfTime,RotationMatrixData],axis = 1)

dfRotation.to_csv("PelvisRotationMatrix.csv", index = False)

#df1 = df[1:2].values
#print(df1)
