import numpy as np
import pandas as pd

def Member(motion_num):
    OpenPoseJoint = ["RSholder","LSholder","MidHip",\
    "RHip","LHip","RWrist","RElbow","LElbow","LWrist"]
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
    RWrist_D = np.eye(motion_num)
    RElbow_D = np.eye(motion_num)
    LElbow_D = np.eye(motion_num)
    LWrist_D = np.eye(motion_num)
    Dis_Mat_list = (RSholder_D,LSholder_D,\
    MidHip_D,RHip_D,LHip_D,RWrist_D,RElbow_D,LElbow_D,LWrist_D)
    return OpenPoseJoint,bodycolumns,Dis_Mat_list
