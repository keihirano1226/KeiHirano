import sys
import glob
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import os
import re
import pandas as pd

basepass = sys.argv[1]
pngpass = basepass + "/depth/"
jpgpass = basepass + "/color/"
depthpass = basepass + "/Exdepth/"
colorpass = basepass + "/Excolor/"
"""
colorfilelist = glob.glob(jpgpass)
colorfilelist.sort()
depthfilelist = glob.glob(jpgpass)
depthfilelist.sort()
"""


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
startFrame = 923
EndFrame = 963
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
j = 0
for i in range(startFrame,EndFrame + 1):
    print("今回の数は" + str(i) + "です")
    ColorImage = cv2.imread(jpgpass + str(i).zfill(10) + ".jpg")
    depthImage = cv2.imread(pngpass + str(i).zfill(10) + ".png",2)
    cv2.imwrite(colorpass + str(j).zfill(10) + '.jpg',ColorImage)
    cv2.imwrite(depthpass + str(j).zfill(10) + '.png',depthImage)
    j += 1
