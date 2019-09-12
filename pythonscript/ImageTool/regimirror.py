# depthとjpgが左右反転しているので、その左右反転を戻すためのスクリプト

import glob
import sys
from PIL import Image, ImageOps
from tqdm import tqdm
basePath = sys.argv[1]

i = 0
filelist = glob.glob(basePath+'/regi/*.jpg')
filelist.sort()
for filename in tqdm(filelist):
    im = Image.open(filename)
    im_mirror = ImageOps.mirror(im)
    im_mirror.save(basePath+'/regi_mirror/'+str(i).zfill(10) + '.jpg')
    i +=1
