#DLT, matlab 'DLT.m,CameraParameter.m" to python
#2019.09.30 Tsubasa Nose

import numpy as np
import glob
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import sys
from BodyColumn import All_joint as AJ

#https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md


def plotPosture(posedata1,posedat2):
    jointPairs = [(0,1),(0,10),(10,9),(1,11),(11,12),(0,3),(3,5),(5,7),(1,4),(4,6),(6,8),(2,3),(2,4)]
    #0:右肩,1:左肩，2:骨盤中央,3:右骨盤,4:左骨盤,5:右手首,6:右肘,7:左肘,8:左手首
    #(右肩，左肩),(右肩，右肘),(右肘，右手首),(左肩，左肘),(左肘，左手首),(骨盤中央,骨盤右),(骨盤中央，骨盤左)，(右肩，骨盤右)，(左肩，骨盤左)
    #plotposture関数が一番描画を考える上では一番重要な関数
    fig = plt.figure()
    ax = Axes3D(fig)
    #関節の座標値の入り方に注意
    #for frame in range(len(posedata)//15):
    for frame in range(int(len(posedata1))):
        #全部で500フレームあるので、間引きして早送りで再生できるようにするスクリプト
        Frame_Pose1 = posedata1[5*frame:5*frame+1]
        Frame_Pose2 = posedata2[5*frame:5*frame+1]
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
        """
        #特徴関節の経路を点線で描画するもの
        for Feature_joint in Feature_joint_list:
            X1 = posedata1.iloc[:,[3*Feature_joint+1]].values.flatten()
            Y1 = posedata1.iloc[:,[3*Feature_joint+2]].values.flatten()
            Z1 = posedata1.iloc[:,[3*Feature_joint+3]].values.flatten()
            ax.plot(X1,Y1,Z1,linewidth = 2,linestyle="solid",color = "orange")
            X2 = posedata2.iloc[:,[3*Feature_joint+1]].values.flatten()
            Y2 = posedata2.iloc[:,[3*Feature_joint+2]].values.flatten()
            Z2 = posedata2.iloc[:,[3*Feature_joint+3]].values.flatten()
            ax.plot(X2,Y2,Z2,linewidth = 2,linestyle="solid",color = "deepskyblue")
        #特徴関節の経路を点線で描画するもの
        origins = [[0,0,0],[0,0,-0.2],[0,0.85,-0.2],[-0.45,0,-0.2],[-0.45,0.85,-0.2],\
        [0,0,0.25],[0,0.85,0.25]]
        lengths = [[0.5,0.9,0.2],[0.05,0.05,0.5],[0.05,0.05,0.5],[0.05,0.05,0.5],[0.05,0.05,0.5],\
        [0.5,0.05,0.25],[0.5,0.05,0.25]]
        i = 0
        color1 = "ivory"
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
        #ax.view_init(elev = 0, azim = -90)
        ax.view_init(elev = 0, azim = -90)
        plt.savefig("/home/kei/document/video3/" + str(frame).zfill(10) + ".png")
        plt.cla()
        """
        plt.pause(0.1)
        #plt.pause(10)
        plt.cla()
        """
if __name__ == '__main__':
    basepass = sys.argv[1]
    OpenPoseJoint,bodycolumns,Dis_Mat_list = AJ.Member(13)
    posepass1 = basepass + "AveragePose1.csv"
    posedata = pd.read_csv(posepass1)
    posedata1 = posedata[bodycolumns]
    posepass2 = basepass + "AveragePose2.csv"
    posedata = pd.read_csv(posepass2)
    posedata2 = posedata[bodycolumns]
    framepass = "/home/kei/document/experiments/method/subject2/motion1/2/UnifiedPose.csv"
    df3 = pd.read_csv(framepass)
    frame = df3.Frame
    posedata1 = pd.concat([frame,posedata1],axis =1)
    posedata2 = pd.concat([frame,posedata2],axis =1)
    plotPosture(posedata1,posedata2)
    print(posedata1)
    posedata1.to_csv("/home/kei/document/experiments/method/subject2/motion1/2/test.csv")
