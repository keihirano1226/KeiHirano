import glob
import sys
import pandas as pd

csvfile = sys.argv[1] + "2DFiltered.csv"
df = pd.read_csv(csvfile)
df = df.drop('time', axis = 1)
df.to_csv(sys.argv[1] + 'test.csv', index = 0,header = 0)
