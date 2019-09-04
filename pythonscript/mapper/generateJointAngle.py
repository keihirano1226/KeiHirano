import pandas as pd
import numpy as np
import sys
from joint_vector import JointVector
from body_columns import MainJointAngleList, joint2coordinate

"""全部の動作を使った場合
subject2 = ((2,3,7,8),(4,5),(1,2,5,6,7))
subject3 = ((1,2,3,4,6),(1,2,3,4,5),(1,2,3,4,5))
subject4 = ((1,2,3,5,7),(1,2,3,7),(1,2,4,6,7))
"""
#1と3だけ使った場合
subject2 = ((2,3,7,8),(),(1,2,5,6,7))
subject3 = ((1,2,3,4,6),(),(1,2,3,4,5))
subject4 = ((1,2,3,5,7),(),(1,2,4,6,7))

subjectlist = (subject2, subject3,subject4)

i = 2
#全関節座標データから関節角を算出
for subject in subjectlist:
    j = 1
    for motion in subject:
        for num in motion:
            csvpass = sys.argv[1] + "subject" + str(i) + "/motion" + str(j) + "/" + str(num) + "/UnifiedPose.csv"
            # print(csvpass)
            unidf = pd.read_csv(csvpass)
            jointdf = pd.DataFrame()
            for sp, gp1, gp2 in MainJointAngleList:
                #関節角への変換
                jv = JointVector(unidf[joint2coordinate(sp)].values,
                                unidf[joint2coordinate(gp1)].values,
                                unidf[joint2coordinate(gp2)].values)
                jointdf[sp] = jv.compute_angle()
            jointdf.to_csv(sys.argv[1] + "subject" + str(i) + "/motion" + str(j) + "/" + str(num) + "/JointAngle.csv",index = 0)
        j+=1
    i+=1