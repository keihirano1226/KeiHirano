# depthとjpgが左右反転しているので、その左右反転を戻すためのスクリプト

import glob
import sys
from PIL import Image, ImageOps
from tqdm import tqdm
basePath = sys.argv[1]

filelist = glob.glob(basePath+'/regi2/*.jpg')
filelist.sort()
for i, filename in enumerate(tqdm(filelist)):
    im = Image.open(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath + 'regi_mirror/' + str(i).zfill(10) + '.jpg')

filelist = glob.glob(basePath+'/depth/*.png')
filelist.sort()
for k, filename in enumerate(tqdm(filelist)):
    im = Image.open(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath + 'depth_mirror/' + str(k).zfill(10) + '.png')
