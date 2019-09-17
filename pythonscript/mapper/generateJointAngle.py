import pandas as pd
import numpy as np
import sys
from BodyColumn import body_columns as bc
from BodyColumn import joint_vector
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
            for sp, gp1, gp2 in bc.MainJointAngleList:
                #関節角への変換
                jv = joint_vector.JointVector(unidf[bc.joint2coordinate(sp)].values,
                                unidf[bc.joint2coordinate(gp1)].values,
                                unidf[bc.joint2coordinate(gp2)].values)
                jointdf[sp] = jv.compute_angle()
            jointdf.to_csv(sys.argv[1] + "subject" + str(subject_index) + "/motion" + str(motion_index) + "/" + str(num) + "/JointAngle.csv",index = 0)

print("関節角を算出しました")