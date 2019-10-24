import sys
import os
#sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from BodyColumn.body_columns import KinectJoint, map2openpose

isFixed = 1 #アフィン変換されているか否か

if __name__ == '__main__':
    basepass = sys.argv[1]
    depthimage_pass = basepass + "depth_mirror/0000000001.tiff"
    csvpass = sys.argv[1] + "/pos/pos.csv"
    df = pd.read_csv(csvpass, header = None)
    df = df.drop(df.columns[[0,1]], axis=1)
    kinect_joint = np.array([])
    flamecnt = 200
    for cnt in tqdm(range(flamecnt)):
        pose = df[cnt:cnt+1].values
        pose_matrix = pose.reshape([int(pose.shape[1]/3),3])
        # depth_image =cv2.imread(depthimage_pass,cv2.IMREAD_COLOR)
        # print(pose_matrix)
        trans_vec = pose_matrix[:,2:]
        trans_vec_inv = 1 / trans_vec
        trans_mat = np.concatenate([trans_vec_inv,trans_vec_inv,trans_vec_inv],axis=1)
        pose_matrix_trans = np.multiply(pose_matrix,trans_mat)
        projection_matrix = np.array([[-365.2995,0,256.106689],[0,-365.2995,208.944901]])
        pose_matrix_2D = np.dot(projection_matrix,pose_matrix_trans.T)
        pose_matrix_2D = pose_matrix_2D.T
        pose_dict = dict(zip(KinectJoint, pose_matrix_2D))
        # print(pose_dict)

        kinect_joint = np.concatenate([kinect_joint, pose_dict['SHOULDER_RIGHT'], pose_dict['SHOULDER_LEFT']])

    if isFixed:
        df = pd.read_csv(sys.argv[1] + "/output_fixed.csv") 
    else:
        df = pd.read_csv(sys.argv[1] + "/output.csv") 
    
    x = np.linspace(0,flamecnt,flamecnt)
    kinect_joint = np.reshape(kinect_joint, (flamecnt, 4))
    fig = plt.figure(1)
    plt.suptitle("Posture estimation error of openpose and kinect in shoulder coordinates")
    plt.subplot(121)
    g1 = plt.plot(x,kinect_joint[:,0])
    f1 = plt.plot(x,df[0:flamecnt].iloc[:, df.columns.str.startswith(map2openpose['SHOULDER_RIGHT'])].values[:,0], linestyle = "dashed")
    g3 = plt.plot(x,kinect_joint[:,2])
    f3 = plt.plot(x,df[0:flamecnt].iloc[:, df.columns.str.startswith(map2openpose['SHOULDER_LEFT'])].values[:,0], linestyle = "dashed")
    plt.legend((g1[0], g3[0], f1[0], f3[0]), ("SRx", "SLx", "SRx(openpose)", "SLx(openpose)"), bbox_to_anchor=(0, -0.2), loc='upper left', borderaxespad=0)
    plt.ylabel("x pixel")
    plt.xlabel("number of flame")
    plt.gcf().subplots_adjust(bottom=0.30)
    plt.subplot(122)
    g2 = plt.plot(x,kinect_joint[:,1])
    f2 = plt.plot(x,df[0:flamecnt].iloc[:, df.columns.str.startswith(map2openpose['SHOULDER_RIGHT'])].values[:,1], linestyle = "dashed")
    g4 = plt.plot(x,kinect_joint[:,3])
    f4 = plt.plot(x,df[0:flamecnt].iloc[:, df.columns.str.startswith(map2openpose['SHOULDER_LEFT'])].values[:,1], linestyle = "dashed")
    plt.legend((g2[0], g4[0], f2[0], f4[0]), ("SRy", "SLy", "SRy(openpose)", "SLy(openpose)"), bbox_to_anchor=(0, -0.2), loc='upper left', borderaxespad=0)
    plt.ylabel("y pixel")
    plt.xlabel("number of flame")
    fig.tight_layout()
    plt.gcf().subplots_adjust(bottom=0.35)
    plt.subplots_adjust(top=0.9)
    fig.align_labels()
    if isFixed:
        plt.savefig(sys.argv[1] + '/diff_fixed.png') 
    else:
        plt.savefig(sys.argv[1] + '/diff.png')
    
    # print(df[0:10].iloc[:, df.columns.str.startswith(map2openpose['SHOULDER_RIGHT'])].values)