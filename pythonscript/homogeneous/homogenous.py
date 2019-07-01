import pandas as pd
import numpy as np
import sys

mocap = sys.argv[1] + "mocap.csv"
Kinect = sys.argv[1] + "Kinect.csv"
Ground = sys.argv[1] + "GroundPoints.csv"
mocapdf = pd.read_csv(mocap)
Kinectdf = pd.read_csv(Kinect)
Grounddf = pd.read_csv(Ground)
#mocapdata = mocapdf.values
Kinectdata = Kinectdf.values
homomocap = mocapdf.assign(D=1)
mocapdata = homomocap.values

A = np.dot(np.linalg.inv(np.dot(mocapdata.T, mocapdata)), mocapdata.T)
homoMatrix = np.dot(A,Kinectdata)
Groundhomo = Grounddf.assign(D = 1)
KinectGround = np.dot(Groundhomo,homoMatrix)
GroundData = pd.DataFrame(KinectGround)
GroundData.columns = ["x","y","z"]
GroundData.index = ["Ground0","Ground1","Ground2"]
pd.to_csv(sys.argv[1] + "KinectGround.csv")
