import pandas as pd
import numpy as np
import sys
import glob
from BodyColumn import Upper_joint as UJ
basepass = sys.argv[1]
pose1 = pd.read_csv(basepass + "AveragePose1.csv")
pose2 = pd.read_csv(basepass + "AveragePose2.csv")
Distance_Mat = np.zeros((1,int(len(pose1.columns)/3)))
diff = pose1-pose2
diff_Mat = diff.values
for i in range(int(len(pose1.columns)/3)):
    joint_diff = diff_Mat[:,3*i:3*i+2]
    diff_vec = np.diag(np.dot(joint_diff,joint_diff.T))
    Distance_Mat[0,i] = np.sum(np.sqrt(diff_vec))

print(Distance_Mat)
OpenPoseJoint,bodycolumns,Dis_Mat_list = UJ.Member(7)
df = pd.DataFrame(Distance_Mat,columns = OpenPoseJoint)
df.to_csv(sys.argv[1] + "Feature_order.csv")
