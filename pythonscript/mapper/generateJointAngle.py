import pandas as pd
import numpy as np
import sys
from joint_vector import JointVector
from body_columns import MainJointAngleList, joint2coordinate
from tqdm import tqdm
from subject_list import subjectlist

#全関節座標データから関節角を算出
print("全関節座標データから関節角を計算中...")
for subject_index, subject in enumerate(tqdm(subjectlist), 2):
    for motion_index, motion in enumerate(subject,1):
        for num in motion:
            csvpass = sys.argv[1] + "subject" + str(subject_index) + "/motion" + str(motion_index) + "/" + str(num) + "/UnifiedPose.csv"
            unidf = pd.read_csv(csvpass)
            jointdf = pd.DataFrame()
            for sp, gp1, gp2 in MainJointAngleList:
                #関節角への変換
                jv = JointVector(unidf[joint2coordinate(sp)].values,
                                unidf[joint2coordinate(gp1)].values,
                                unidf[joint2coordinate(gp2)].values)
                jointdf[sp] = jv.compute_angle()
            jointdf.to_csv(sys.argv[1] + "subject" + str(subject_index) + "/motion" + str(motion_index) + "/" + str(num) + "/JointAngle.csv",index = 0)

print("関節角を算出しました")