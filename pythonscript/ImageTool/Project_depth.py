import sys
import os
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import numpy as np
import pandas as pd
from tqdm import tqdm

def depth_projection(pose_matrix,depth_image):
    trans_vec = pose_matrix[:,2:]
    trans_vec_inv = 1 / trans_vec
    trans_mat = np.concatenate([trans_vec_inv,trans_vec_inv,trans_vec_inv],axis=1)
    pose_matrix_trans = np.multiply(pose_matrix,trans_mat)
    projection_matrix = np.array([[-365.2995,0,256.106689],[0,-365.2995,208.944901]])
    pose_matrix_2D = np.dot(projection_matrix,pose_matrix_trans.T)
    pose_matrix_2D = pose_matrix_2D.T
    projected_depth = depth_image
    for i in range(pose_matrix_2D.shape[0]):
        [u,v] = pose_matrix_2D[i]
        projected_depth = cv2.circle(projected_depth,(int(u),int(v)),5,(0,255,0))

    return projected_depth

if __name__ == '__main__':
    basepass = sys.argv[1]
    depthimage_pass = basepass + "/render/0000000000_rendered.png"
    csvpass = sys.argv[1] + "/pos/pos.csv"
    df = pd.read_csv(csvpass, header = None)
    df = df.drop(df.columns[[0,1]], axis=1)
    #print(df[0:1])
    pose = df[0:1].values
    pose_matrix = pose.reshape([int(pose.shape[1]/3),3])
    depth_image =cv2.imread(depthimage_pass,cv2.IMREAD_COLOR)
    print(pose_matrix)
    projected_depth = depth_projection(pose_matrix,depth_image)
    cv2.imwrite(basepass + "/test.jpg",projected_depth)

    #print(projected_depth)
