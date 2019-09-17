import numpy as np
from subject_list import motion_num
#距離行列計算用
OpenPoseJoint = ["Neck","RSholder","LSholder","RElbow","LElbow","LWrist","RWrist","MidHip","RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
bodycolumns = []

RSholder_D = np.zeros((motion_num, motion_num))
LSholder_D = np.zeros((motion_num, motion_num))
RElbow_D = np.zeros((motion_num, motion_num))
LElbow_D = np.zeros((motion_num, motion_num))
RHip_D = np.zeros((motion_num, motion_num))
LHip_D = np.zeros((motion_num, motion_num))
RKnee_D = np.zeros((motion_num, motion_num))
LKnee_D = np.zeros((motion_num, motion_num))
Dis_Mat_list = [RSholder_D, RElbow_D, RHip_D, RKnee_D, LSholder_D,LElbow_D, LHip_D, LKnee_D]

MainJointAngleList = [['RSholder', 'Neck', 'RElbow'], ['RElbow', 'RSholder', 'RWrist'], ['RHip', 'MidHip', 'RKnee'], ['RKnee', 'RHip', 'RAnkle'],
                      ['LSholder', 'Neck', 'LElbow'], ['LElbow', 'LSholder', 'LWrist'], ['LHip', 'MidHip', 'LKnee'], ['LKnee', 'LHip', 'LAnkle']]
for point in OpenPoseJoint:
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        bodycolumns.append(newcolumn)

#関節名から関節座標名への変換
def joint2coordinate(name):
    return list(map(lambda x : name + x, Coordinate))

