import numpy as np
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

tifffolderpass = "./tiff1/"
"""
for i in range(65536):
    #print(i)
    blank = i * np.ones((424,512,1))
    cv2.imwrite(tifffolderpass + str(i) + '.png', blank)
"""
