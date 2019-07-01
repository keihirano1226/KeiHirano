import pandas as pd
import numpy as np
df = pd.read_csv('Coordinate.csv')
center = pd.concat([df.X41,df.Y41,df.Z41],axis = 1)
center = center.rename(columns = {'X41':'X','Y41':'Y','Z41':'Z'})
ColumnList = df.columns.values
#print(type(ColumnList[0]))
dfall = df.Time
for i in range(15):
	print(i)
	df1 = df.iloc[:,3*i+1:3*i+4]
	#xtest = 'X' + str(3*i+1)
	#ytest = 'Y' + str(3*i+2)
	#ztest = 'Z' + str(3*i+3)
	xtest = ColumnList[3*i + 1]
	ytest = ColumnList[3*i + 2]
	ztest = ColumnList[3*i + 3]
	print(type(xtest))
	#df1 = df1.rename(columns = {'X' + str(3*i+1):'X','Y' + str(3*i+2):'Y','Z' + str(3*i+3):'Z'})
	df3 = df1.rename(columns = {xtest:'X',ytest:'Y',ztest:'Z'})
	print(df3)
	df2 = df3.sub(center)
	#pd.concat([df.X41,df.Y41,df.Z41],axis = 1)
	dfall = pd.concat([dfall,df2],axis = 1)
dfall.to_csv("centered.csv")