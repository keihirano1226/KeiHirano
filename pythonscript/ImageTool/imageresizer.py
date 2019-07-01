import sys
import glob
from PIL import Image
import os
"""
img = Image.open('0000000001.jpg')
width,height = 1920,1080
img = img.resize((width,height))
img.save('001_resize.jpg')
"""
image_file_pass = sys.argv[1] + 'jpg/*.jpg'
image_file_list = glob.glob(image_file_pass)
image_file_list.sort()
#os.mkdir('./resized')
print(image_file_list)
i = 1
for image in image_file_list:
    img = Image.open(image)
    width,height = 1920,1080
    img = img.resize((width,height))
    img.save(sys.argv[1] + 'color/'+ str(i).zfill(10) + '.jpg')
    i += 1
