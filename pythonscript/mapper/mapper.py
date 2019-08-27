import pandas as pd
import numpy as np
import seaborn as sns
import sys
import matplotlib.pyplot as plt
from Make_Feature import Extractor
from sklearn import manifold
from scipy.spatial import distance
from polar import Coortra
import mca
from sklearn.manifold import TSNE
basepass = "/home/kei/document/experiments/ICTH2019/"
subjectnamelist = ["SY","Hino","SK"]
Times = [5,1,3]
Feature_Flag = [0,1,0]
OpenPoseJoint = ["Neck","LSholder","RElbow","LElbow","LWrist","MidHip",\
"RHip","LHip","RKnee","LKnee","RAnkle","LAnkle"]
Coordinate = ["X","Y","Z"]
Coordinate2 = ["theta","phi"]
columns = []
selectpartscolumns = []
for point in OpenPoseJoint:
    for coordinate in Coordinate2:
        newcolumn = point + coordinate
        columns.append(newcolumn)
    for coordinate in Coordinate:
        newcolumn = point + coordinate
        selectpartscolumns.append(newcolumn)
print(sum(Feature_Flag))
i = 0
for subject in subjectnamelist:
    time = Times[i]
    for number in range(time):
        if i == 0 and number == 0:
            print(number)
            csvpass = basepass + subject + "/" + subject + str(number + 1) + ".csv"
            df = pd.read_csv(csvpass, index_col=0)
            selectedparts = df[selectpartscolumns]
            polardata = Coortra.DimentionUni(selectedparts,1)
            df2 = pd.DataFrame(polardata,columns = selectpartscolumns)
            featurevector = Extractor.Feature(df2,Feature_Flag)
            featurevector = pd.DataFrame(featurevector, columns = [subject + str(number + 1)])
            #print(featurevector)
            print("iの値は" +str(i))
            beforefeature = featurevector
        else:
            print(number)
            csvpass = basepass + subject + "/" + subject + str(number + 1) + ".csv"
            df = pd.read_csv(csvpass, index_col=0)
            selectedparts = df[selectpartscolumns]
            polardata = Coortra.DimentionUni(selectedparts,1)
            df2 = pd.DataFrame(polardata,columns = selectpartscolumns)
            featurevector = Extractor.Feature(df2,Feature_Flag)
            #print(featurevector)
            #featurevector.column = [subject + str(number + 1)]
            featurevector = pd.DataFrame(featurevector, columns = [subject + str(number + 1)])
            print(featurevector)
            print("iの値は" +str(i))
            beforefeature = pd.concat([beforefeature,featurevector], axis = 1)
    i = i+1
dfall = beforefeature.T
corr = dfall.corr()
corr.head(len(corr))
corr.to_csv( basepass + '/result_dev/time_table.csv')
print(corr)
#sns.heatmap(corr, center = 0, square = True, vmax = 1, vmin = -1)
#plt.savefig(basepass + 'all_fig.png')
dfall.to_csv(basepass + "/result_dev/dev_FeatureMatrix.csv")
tsne = TSNE(n_components = 2, random_state=42)
data_tsne = tsne.fit_transform(dfall)
plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams['font.size'] = 10 #フォントサイズを設定
plt.scatter(data_tsne[:, 0], data_tsne[:, 1], c = "b", marker= "o")
labels = dfall.index

for label,x,y in zip(labels,data_tsne[:,0],data_tsne[:,1]):
    plt.annotate(label,xy = (x, y))
plt.savefig("/home/kei/document/experiments/ICTH2019/result_dev/dev_tsne_map.png")
