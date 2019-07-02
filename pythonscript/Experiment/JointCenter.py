import pandas as pd
import numpy as np
import sys

class jointpairs:
    def __init__(self,Coordinatedata,joint,direction1,direction2):
        self.Coordinate = ["x","y","z"]
        self.direction1 = direction1
        self.direction2 = direction2
        self.joint = joint
        self.jointdata1columns = [self.joint + self.direction1 + "x", self.joint + self.direction1 + "y", self.joint + self.direction1 + "z"]
        self.jointdata2columns = [self.joint + self.direction2 + "x", self.joint + self.direction2 + "y", self.joint + self.direction2 + "z"]
        self.Coordinatedata = Coordinatedata
        self.jointdata1 = self.Coordinatedata[self.jointdata1columns]
        self.jointdata2 = self.Coordinatedata[self.jointdata2columns]
    def JointRadius(self):
        radiusvec = self.jointdata1.values - self.jointdata2.values
        radiusMat = np.dot(radiusvec,radiusvec.T)
        radiusDistancevec = np.sqrt(np.diag(radiusMat))
        radiusDistancevec2 = np.reshape(radiusDistancevec, (len(radiusDistancevec),1))
        return radiusDistancevec2 /2
mocapfilepass = "/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "mocaptrans.csv"
mocap = pd.read_csv(mocapfilepass)
OpenPoseErrorpass = "/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "OpenPoseError.csv"
OpenPoseError = pd.read_csv(OpenPoseErrorpass)
KinectErrorpass = "/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "KinectError.csv"
KinectError = pd.read_csv(KinectErrorpass)
mocapJoint = ["neck","Rshoulder","Lshoulder","Relbow","Lelbow","Rwrist","Lwrist","pelvis","RHip",\
"LHip","Rknee","Lknee","Rankle","Lankle"]
Coordinate = ["x","y","z"]
mocapcolumns = []
for point in mocapJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        mocapcolumns.append(newcolumn)
torsocolumns = []
torsomarkers = ["neck","Rshoulder","Lshoulder","Rpelvis",\
"Lpelvis","pelvis"]
limbmarkers = ["Relbow","Lelbow","Rwrist","Lwrist","Rknee","Lknee","Rankle","Lankle"]
OpenPoseErrorcolumns = []
Method = ["OpenPose_"]#,"OpenPose_","OpenPoseBack_"]
ErrorJoint = ["Neck","RShoulder","Lshoulder","RElbow","LElobow","RWrist","LWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle","MPJPE"]
Distance = ["Euclidean"]
for method in Method:
    for point in ErrorJoint:
        for distance in Distance:
            newcolumn = method + point + distance
            OpenPoseErrorcolumns.append(newcolumn)
KinectErrorcolumns = []
Method = ["Kinect_"]#,"OpenPose_","OpenPoseBack_"]
ErrorJoint = ["Neck","RShoulder","Lshoulder","RElbow","LElobow","RWrist","LWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle","MPJPE"]
Distance = ["Euclidean"]
for method in Method:
    for point in ErrorJoint:
        for distance in Distance:
            newcolumn = method + point + distance
            KinectErrorcolumns.append(newcolumn)
#誤差の原因として，大きく乗っている誤差が体の厚みによるシフト誤差であるということを言うことが重要
Errors = OpenPoseError[OpenPoseErrorcolumns]
KinectErrors = KinectError[KinectErrorcolumns]
print(Errors.mean())
errormean = Errors.mean()
errorstd = Errors.std()
KinectErrormean = KinectErrors.mean()
Kinectstd = KinectErrors.std()
print(type(Errors))
print(type(errormean))
errormean1 = errormean.T
errorstd1 = errorstd.T
Kinecterrormean1 = KinectErrormean.T
Kinecterrorstd1 = Kinectstd.T
print(errormean1)
error = pd.concat([errormean,errorstd],axis = 1)
Kinecterror1 = pd.concat([KinectErrormean,Kinectstd],axis = 1)
columns = ["mean","std"]
error.columns = columns
Kinecterror1.columns = columns
"""
neckcal = jointpairs(mocap,"neck","F","B")
neckradi = neckcal.JointRadius()
print(neckradi)
"""
radiusMat = np.zeros((len(mocap),14))
j = 0
for marker in torsomarkers:
    jointcal = jointpairs(mocap,marker,"F","B")
    radius = jointcal.JointRadius()
    radiusMat[:,j:j+1] = radius
    j += 1
for marker1 in limbmarkers:
    jointcal = jointpairs(mocap,marker1,"in","out")
    radius = jointcal.JointRadius()
    radiusMat[:,j:j+1] = radius
    j += 1
RadiusData = pd.DataFrame(radiusMat,columns = torsomarkers + limbmarkers)
#カラムの並び替え作業
Radius = ["neck","Rshoulder","Lshoulder","Relbow","Lelbow","Rwrist","Lwrist","pelvis",\
"Rpelvis","Lpelvis","Rknee","Lknee","Rankle","Lankle"]
#カラムの並び替え作業
RadiusData2 = RadiusData[Radius]
RadiusData1 = RadiusData2[0:1].values.T
print(RadiusData1)
RadiusData2.to_csv("/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "各関節の関節半径.csv")
error.to_csv("/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "OpenPoseの誤差平均と分散.csv")
Kinecterror1.to_csv("/home/kei/document/experiments/2019.06.06/計算用フォルダ/" + sys.argv[1] + "Kinectの誤差平均と分散.csv")
#print(Errors.std)
