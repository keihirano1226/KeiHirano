import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

experimentdatapass = "/home/kei/document/experiments/2019.06.06/backwalk/"
csvfile = experimentdatapass + "Yaxis3D.csv"
df = pd.read_csv(csvfile)
pca = PCA(n_components=1)
feature = pca.fit(df)
feature = pca.transform(df)
print(pca.components_[0])
pca1 = pca.components_[0].reshape([1,3])
print(pca1)
df = pd.DataFrame(pca1,columns = ["X","Y","Z"])
df.to_csv(experimentdatapass + "YaxisVec.csv", index = 0)
