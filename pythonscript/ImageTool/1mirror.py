# depthとjpgが左右反転しているので、その左右反転を戻すためのスクリプト

import glob
import sys
from PIL import Image, ImageOps

#basePath = sys.argv[1]

i = 0
"""
filelist = glob.glob(basePath+'/regi2/*.jpg')
filelist.sort()
for filename in filelist:
    im = Image.open(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath+'/regi_mirror/'+str(i).zfill(10) + '.jpg')
    i +=1
"""
im = Image.open("/home/kei/document/experiments/2019.06.21/data4/test/0000001135.jpg")
im_mirror = ImageOps.mirror(im)
im_mirror.save("/home/kei/document/experiments/2019.06.21/data4/test/mirror.jpg")
