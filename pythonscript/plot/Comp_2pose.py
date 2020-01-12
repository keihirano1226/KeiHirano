import numpy as np
import glob
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import sys


#https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md


def plotPosture(posedata1,posedata2):
    #jointPairs = [(0,1), (0,6), (6,5), (1,7), (7,8), (2,3), (2,4), (0,3),(1,4)]
    jointPairs = [(0,1),(1,2),(2,3),(3,4),(1,5),(5,6),(6,7),(1,8),(8,9),(9,10),(10,11),(8,12),(12,13),(13,14)]
    #0:鼻,1:首，2:右肩,3:右肘,4:右手首,5:左肩,6:左肘,7:左手首,8:骨盤中央,9:右骨盤,10:右膝,11:右足首,12:左骨盤,13:左膝,14:左足首
    #(鼻，首),(首，右肩),(右肩，右肘),(右肘，右手首),(首，左肩),(左肩,左肘),(左肘，左手首)，(右肩，骨盤右)，(骨盤右，右膝),(右膝，右足首),\
    #(左肩，骨盤左),(骨盤左，左膝),(左膝，左足首)
    #plotposture関数が一番描画を考える上では一番重要な関数
    fig = plt.figure()
    ax = Axes3D(fig)
    #関節の座標値の入り方に注意
    #for frame in range(len(posedata)//15):
    for frame in range(int(len(posedata1))):
        #全部で500フレームあるので、間引きして早送りで再生できるようにするスクリプト
        Frame_Pose1 = posedata1[5*frame:5*frame+1]
        Frame_Pose2 = posedata2[5*frame:5*frame+1]
        Frame_Pose1 = posedata1[1*frame:1*frame+1]
        Frame_Pose2 = posedata2[1*frame:1*frame+1]
        X = []
        Y = []
        Z = []
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        #関節同士を実線で結ぶ部分
        for i,j in jointPairs:
            lineX1 = []
            lineY1 = []
            lineZ1 = []
            lineX1.append(Frame_Pose1.iat[0,3*i+1])
            lineY1.append(Frame_Pose1.iat[0,3*i+2])
            lineZ1.append(Frame_Pose1.iat[0,3*i+3])
            lineX1.append(Frame_Pose1.iat[0,3*j+1])
            lineY1.append(Frame_Pose1.iat[0,3*j+2])
            lineZ1.append(Frame_Pose1.iat[0,3*j+3])
            ax.plot(lineX1, lineY1, lineZ1, marker='None', linestyle='-',color = "red")
            lineX2 = []
            lineY2 = []
            lineZ2 = []
            lineX2.append(Frame_Pose2.iat[0,3*i+1])
            lineY2.append(Frame_Pose2.iat[0,3*i+2])
            lineZ2.append(Frame_Pose2.iat[0,3*i+3])
            lineX2.append(Frame_Pose2.iat[0,3*j+1])
            lineY2.append(Frame_Pose2.iat[0,3*j+2])
            lineZ2.append(Frame_Pose2.iat[0,3*j+3])
            ax.plot(lineX2, lineY2, lineZ2, marker='None', linestyle='-',color = "blue")
        #関節同士を実線で結ぶ部分
        origins = [[0,0,0],[0,0,-0.2],[0,0.85,-0.2],[-0.45,0,-0.2],[-0.45,0.85,-0.2],\
        [0,0,0.25],[0,0.85,0.25]]
        lengths = [[0.5,0.9,0.2],[0.05,0.05,0.5],[0.05,0.05,0.5],[0.05,0.05,0.5],[0.05,0.05,0.5],\
        [0.5,0.05,0.25],[0.5,0.05,0.25]]
        i = 0
        color1 = "ivory"
        """
        for origin in origins:
            length = lengths[i]
            #origin = [0,0,0]
            #length = [0.5,0.5,0.2]
            #ここから直方体を書くfor文の中身用の処理
            x = [origin[0]-length[0],origin[0]]
            y = [origin[1],origin[1]+length[1]]
            z = [origin[2]-length[2],origin[2]]
            alpha1 = 0.3
            X,Y = np.meshgrid(x,y)
            Z1 = np.array([[origin[2]-length[2], origin[2]-length[2]], [origin[2]-length[2], origin[2]-length[2]]])
            Z2 = np.array([[origin[2], origin[2]], [origin[2], origin[2]]])
            ax.plot_surface(X,Y,Z1,alpha=alpha1,color = color1)
            ax.plot_surface(X,Y,Z2,alpha=alpha1,color = color1)
            X,Z = np.meshgrid(x,z)
            Y1 = np.array([[origin[1]+length[1], origin[1]+length[1]], [origin[1]+length[1], origin[1]+length[1]]])
            Y2 = np.array([[origin[1], origin[1]], [origin[1], origin[1]]])
            ax.plot_surface(X,Y1,Z,alpha=alpha1,color = color1)
            ax.plot_surface(X,Y2,Z,alpha=alpha1,color = color1)
            Y,Z = np.meshgrid(y,z)
            X1 = np.array([[origin[0]-length[0], origin[0]-length[0]], [origin[0]-length[0], origin[0]-length[0]]])
            X2 = np.array([[origin[0], origin[0]], [origin[0], origin[0]]])
            ax.plot_surface(X1,Y,Z,alpha=alpha1,color = color1)
            ax.plot_surface(X2,Y,Z,alpha=alpha1,color = color1)
            i+=1
            #ここまでで、ひとつの直方体がかける。
        """
        ax.set_xlim(-1,1)
        ax.set_ylim(-1,1)
        ax.set_zlim(-0.5,1.5)
        ax.set_xticks(np.arange(-1, 1, step=0.5))
        ax.set_yticks(np.arange(-1, 1, step=0.5))
        ax.set_zticks(np.arange(0, 1.5, step=0.5))
        ax.view_init(elev = -90, azim = -90)
        plt.savefig("/home/kei/document/pose/" + str(frame).zfill(10) + ".png")
        plt.cla()
        #ax.view_init(elev = 0, azim = -90)
        """
        plt.pause(0.0001)
        #plt.pause(10)
        plt.cla()
        """

if __name__ == '__main__':
    basepass = sys.argv[1]
    posepass1 = basepass + "3DFiltered2.csv"
    posedata1 = pd.read_csv(posepass1)
    posepass2 = basepass + "3DFiltered1.csv"
    posedata2 = pd.read_csv(posepass2)
    Feature_joint_list = [1,2]
    plotPosture(posedata1,posedata2)
