import h5py
import numpy
import pandas as pd
#f = './Directions.h5'
#model = 今回読み取りたいh5ファイルの変数名
model = h5py.File('./cameras.h5','r')
#h5pyの中身はkeyで指定できる。今回は”subject1"ってkeyのみ
print(list(model.keys()))
print(list(model['subject1'].keys()))
print(list(model['subject1']['camera1'].keys()))
"""
x = model['subject1'].value.T
print(model['subject1'].value.shape)
df = pd.DataFrame(x)
print(type(df))
df.to_csv("3dposedata.csv")
"""
