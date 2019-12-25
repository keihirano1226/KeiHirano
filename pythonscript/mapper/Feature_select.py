import pandas as pd
import numpy as np
import sys
from uniframe import resampling as rs
import scipy.spatial.distance as distance
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score, davies_bouldin_score
import glob
from tqdm import tqdm
from BodyColumn import Upper_joint as UJ
from scipy import stats
basepath = "/home/kei/document/experiments/Master/"
posepass = basepath + "Unified/"
class1 = ["no33_5","no33_3","no29_1"]
class2 = ["no33_1","no32_2","no32_3","no9_2","no9_1","no30_1","no33_2","no31_1","no33_4","no32_1","no31_2","no31_3"]
OpenPoseJoint,bodycolumns,Dis_Mat_list = UJ.Member(7)
AveragePose1 = pd.read_csv(posepass + "AveragePose1.csv", index_col = 0)
AveragePose2 = pd.read_csv(posepass + "AveragePose2.csv", index_col = 0)
Distance_Mat1 = np.zeros((len(class1),int(len(AveragePose1.columns)/3)))
Distance_Mat2 = np.zeros((len(class2),int(len(AveragePose1.columns)/3)))

j = 0
for member in class1:
    dfpose = pd.read_csv(posepass + member + ".csv")
    dfpose = dfpose[bodycolumns]
    diff = AveragePose1 - dfpose
    diff_Mat = diff.values
    for i in range(int(len(AveragePose1.columns)/3)):
        joint = diff_Mat[:,3*i:3*i+2]
        diff_vec = np.diag(np.dot(joint,joint.T))
        Distance_Mat1[j,i] = np.sum(np.sqrt(diff_vec))
    j+=1
j = 0
for member in class2:
    dfpose = pd.read_csv(posepass + member + ".csv")
    dfpose = dfpose[bodycolumns]
    diff = AveragePose1 - dfpose
    diff_Mat = diff.values
    for i in range(int(len(AveragePose1.columns)/3)):
        joint = diff_Mat[:,3*i:3*i+2]
        diff_vec = np.diag(np.dot(joint,joint.T))
        Distance_Mat2[j,i] = np.sum(np.sqrt(diff_vec))
    j+=1
df1 = pd.DataFrame(Distance_Mat1,columns = OpenPoseJoint)
df2 = pd.DataFrame(Distance_Mat2,columns = OpenPoseJoint)
df1.to_csv(basepath + "UJ_result/class1_diff.csv")
df2.to_csv(basepath + "UJ_result/class2_diff.csv")
p_Mat = np.zeros((1,int(len(AveragePose1.columns)/3)))
j = 0
# 参考サイト　https://qiita.com/suaaa7/items/745ac1ca0a8d6753cf60
for joint in OpenPoseJoint:
    A = df1[joint].values
    B = df2[joint].values
    print(A)
    print(B)
    A_var = np.var(A, ddof=1)  # Aの不偏分散
    B_var = np.var(B, ddof=1)  # Bの不偏分散
    A_df = len(A) - 1  # Aの自由度
    B_df = len(B) - 1  # Bの自由度
    f = A_var / B_var  # F比の値
    one_sided_pval1 = stats.f.cdf(f, A_df, B_df)  # 片側検定のp値 1
    one_sided_pval2 = stats.f.sf(f, A_df, B_df)   # 片側検定のp値 2
    p = min(one_sided_pval1, one_sided_pval2) * 2  # 両側検定のp値
    print('F:       ', round(f, 3))
    print('p-value: ', round(p, 3))
    if p <0.05:
        a = stats.ttest_ind(A, B, equal_var=False)
        p_Mat[0,j] = a.pvalue
        print(a.pvalue)
    if p >= 0.05:
        a = stats.ttest_ind(A, B)
        p_Mat[0,j] = a.pvalue
        print(a.pvalue)
    j+=1
df = pd.DataFrame(p_Mat, columns = OpenPoseJoint)
df.to_csv(basepath + "UJ_result/Feature_Joint2.csv")
