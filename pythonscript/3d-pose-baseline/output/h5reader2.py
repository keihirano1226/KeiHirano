import h5py
import numpy
import pandas as pd
#f = './Directions.h5'
#model = 今回読み取りたいh5ファイルの変数名
model = h5py.File('./Directions.h5','r')
#h5pyの中身はkeyで指定できる。今回は”3D_positions"ってkeyのみ
print(list(model.keys()))
x = model['3D_positions'].value.T
print(model['3D_positions'].value.shape)
df = pd.DataFrame(x)
print(type(df))
df.to_csv("3dposedata.csv")
