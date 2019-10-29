# depthとjpgが左右反転しているので、その左右反転を戻すためのスクリプト

import glob
import sys
from PIL import Image, ImageOps
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
from tqdm import tqdm
basePath = sys.argv[1]

for filename in tqdm(glob.glob(basePath+'/color/*.jpg')):
    im = Image.open(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath+'/color_mirror/'+filename[-14:])
