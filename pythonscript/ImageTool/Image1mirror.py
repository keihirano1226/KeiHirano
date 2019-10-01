import glob
import sys
from PIL import Image, ImageOps
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
from tqdm import tqdm
image = cv2.imread("/home/kei/document/experiments/BioEngen/MA330_11/regi_test/regi_test.jpg")
image_flip = cv2.flip(image, 1)
cv2.imwrite("/home/kei/document/experiments/BioEngen/MA330_11/regi_test/regi_test_flip.jpg", image_flip)
