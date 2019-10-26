#DLT, matlab 'DLT.m,CameraParameter.m" to python
#2019.09.30 Tsubasa Nose

import numpy as np
import glob
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import sys


#https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md


def plotPosture(posedata):
    jointPairs = [(0,1), (0,6), (6,5), (1,7), (7,8), (2,3), (2,4), (0,3),(1,4)]
    #0:右肩,1:左肩，2:骨盤中央,3:右骨盤,4:左骨盤,5:右手首,6:右肘,7:左肘,8:左手首
    #(右肩，左肩),(右肩，右肘),(右肘，右手首),(左肩，左肘),(左肘，左手首),(骨盤中央,骨盤右),(骨盤中央，骨盤左)，(右肩，骨盤右)，(左肩，骨盤左)
    #plotposture関数が一番描画を考える上では一番重要な関数
    fig = plt.figure()
    ax = Axes3D(fig)
    #関節の座標値の入り方に注意
    #for frame in range(len(posedata)//15):
    for frame in range(int(len(posedata)/5)):
        Frame_Pose = posedata[5*frame:5*frame+1]
        X = []
        Y = []
        Z = []
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        for a in range(9):
            X.append(Frame_Pose.iat[0,3*a+1])
            Y.append(Frame_Pose.iat[0,3*a+2])
            Z.append(Frame_Pose.iat[0,3*a+3])
        for i,j in jointPairs:
            lineX = []
            lineY = []
            lineZ = []
            lineX.append(Frame_Pose.iat[0,3*i+1])
            lineY.append(Frame_Pose.iat[0,3*i+2])
            lineZ.append(Frame_Pose.iat[0,3*i+3])
            lineX.append(Frame_Pose.iat[0,3*j+1])
            lineY.append(Frame_Pose.iat[0,3*j+2])
            lineZ.append(Frame_Pose.iat[0,3*j+3])
            ax.plot(lineX, lineY, lineZ, marker='None', linestyle='-',color = "b")
        seat_x = [-0.5,0]
        seat_y = [0,0.5]
        X,Y = np.meshgrid(seat_x,seat_y)
        Z = np.array([[-0.1, -0.1], [-0.1, -0.1]])
        ax.plot_surface(X,Y,Z,alpha=0.7,color = "saddlebrown")
        #ax.plot_surface(X,Y,-Z,alpha=0.7,color = "saddlebrown")
        """
        ax.plot_surface( X,  Z,  Y, alpha=0.7,color = "saddlebrown")
        ax.plot_surface( X, -Z,  Y, alpha=0.7,color = "saddlebrown")
        ax.plot_surface( Z,  X,  Y, alpha=0.7,color = "saddlebrown")
        ax.plot_surface(-Z,  X,  Y, alpha=0.7,color = "saddlebrown")
        """
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.set_zlim(-0.5,1.5)
        ax.set_xticks(np.arange(-1, 1, step=0.5))
        ax.set_yticks(np.arange(-1, 1, step=0.5))
        ax.set_zticks(np.arange(0, 1.5, step=0.5))

        plt.pause(0.0001)
        #plt.pause(10)
        plt.cla()
if __name__ == '__main__':
    basepass = sys.argv[1]
    posepass = basepass + "AveragePose1.csv"
    posedata = pd.read_csv(posepass)
    plotPosture(posedata)
