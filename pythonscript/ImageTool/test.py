import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import numpy as np
imagepath = "/home/kei/document/experiments/Hamano/H5_3/render/0000000230_rendered.png"
image = cv2.imread(imagepath)
image = cv2.circle(image,(116,264),5,(0,255,0))
image = cv2.circle(image,(141,285),5,(0,255,0))
image = cv2.circle(image,(67,246),5,(0,255,0))
image = cv2.circle(image,(115,250),5,(0,255,0))
#image= cv2.circle(image,(74,388),5,(0,255,0))
cv2.imwrite("test.jpg",image)
