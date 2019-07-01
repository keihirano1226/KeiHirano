import pandas as pd
import numpy as np
import sys
from sklearn.decomposition import PCA

csvfile = sys.argv[1] + "3DInterrupt.csv"
df = pd.read_csv(csvfile)
#進行方向の抽出
Direction = df[["MidHipX","MidHipY","MidHipZ"]]

#進行方向行列に対して、正規化を行う。
dfs = (Direction - Direction.mean()) / Direction.std()
#主成分分析により、進行方向ベクトルを求める
pca = PCA(n_components=2)
feature = pca.fit(dfs)
feature = pca.transform(dfs)
print(pca.components_[0])
print("test")
print(pca.components_[1])
c = np.dot(pca.components_[0], pca.components_[1])
pca1 = pca.components_[0].reshape([1,3])
print(pca1)
df = pd.DataFrame(pca1,columns = ["X","Y","Z"])
df.to_csv(sys.argv[1] + "DirectionVec.csv", index = 0)
