# depthとjpgが左右反転しているので、その左右反転を戻すためのスクリプト

import glob
import sys
from PIL import Image, ImageOps
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

basePath = sys.argv[1]

for filename in glob.glob(basePath+'/color/*.jpg'):
    im = Image.open(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath+'/color_mirror/'+filename[-14:])

for filename in glob.glob(basePath+'/depth/*.png'):
    """
    im = Image.open(filename)
    print(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath+'depth_mirror/'+filename[-15:])
    """
    im_gray = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    im_gray2 = cv2.flip(im_gray, 1)
    cv2.imwrite(basePath + '/depth_mirror/' + filename[-15:], im_gray2)
