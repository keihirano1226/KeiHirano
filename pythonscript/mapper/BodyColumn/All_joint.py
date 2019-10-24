import numpy as np
import pandas as pd
#距離行列計算用
def Member(motion_num):
    OpenPoseJoint = ["RSholder","LSholder","MidHip",\
    "RHip","LHip","RKnee","LKnee","RAnkle","LAnkle","RWrist",\
    "RElbow","LElbow","LWrist"]
    Coordinate = ["X","Y","Z"]
    bodycolumns = []
    for point in OpenPoseJoint:
        for coordinate in Coordinate:
            newcolumn = point + coordinate
            bodycolumns.append(newcolumn)
    #各関節の距離行列の作成


    RSholder_D = np.eye(motion_num)
    LSholder_D = np.eye(motion_num)
    MidHip_D = np.eye(motion_num)
    RHip_D = np.eye(motion_num)
    LHip_D = np.eye(motion_num)
    RKnee_D = np.eye(motion_num)
    LKnee_D = np.eye(motion_num)
    RAnkle_D = np.eye(motion_num)
    LAnkle_D = np.eye(motion_num)
    RWrist_D = np.eye(motion_num)
    RElbow_D = np.eye(motion_num)
    LElbow_D = np.eye(motion_num)
    LWrist_D = np.eye(motion_num)
    Dis_Mat_list = (RSholder_D,LSholder_D,\
    MidHip_D,RHip_D,LHip_D,RKnee_D,LKnee_D,RAnkle_D,\
    LAnkle_D,RWrist_D,RElbow_D,LElbow_D,LWrist_D)
    return OpenPoseJoint,bodycolumns,Dis_Mat_list
    
