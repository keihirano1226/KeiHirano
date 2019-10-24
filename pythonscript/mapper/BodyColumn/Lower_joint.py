import numpy as np
import pandas as pd
#距離行列計算用
def Member(motion_num):
    OpenPoseJoint = ["MidHip","RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
    Coordinate = ["X","Y","Z"]
    bodycolumns = []
    for point in OpenPoseJoint:
        for coordinate in Coordinate:
            newcolumn = point + coordinate
            bodycolumns.append(newcolumn)
    #各関節の距離行列の作成

    MidHip_D = np.eye(motion_num)
    RHip_D = np.eye(motion_num)
    LHip_D = np.eye(motion_num)
    RKnee_D = np.eye(motion_num)
    LKnee_D = np.eye(motion_num)
    RAnkle_D = np.eye(motion_num)
    LAnkle_D = np.eye(motion_num)
    Dis_Mat_list = (MidHip_D,RHip_D,LHip_D,RKnee_D,LKnee_D,RAnkle_D,\
    LAnkle_D)
    return OpenPoseJoint,bodycolumns,Dis_Mat_list
