import pandas as pd
import numpy as np
import sys
import glob
import csv
from scipy import signal
import matplotlib.pyplot as plt

InputFileName = sys.argv[1] + '2DFiltered.csv'
FrameFileName = sys.argv[1] + 'Frame.csv'

df = pd.read_csv(InputFileName)
f = open(FrameFileName, 'r')
reader = csv.reader(f)
#header = next(reader)
i = 0
for row in reader:
    #print(row)
    if i == 0:
        StartFrame = int(row[0])
    elif i == 1:
        EndFrame = int(row[0])
    i += 1
f.close()
dfCutted = df[StartFrame:EndFrame+1]
dfCutted = dfCutted.rename(columns={'Unnamed: 0':'time'})
dfCutted.to_csv(sys.argv[1] + "CutOutput.csv", index = 0)
#print(dfFrame)
