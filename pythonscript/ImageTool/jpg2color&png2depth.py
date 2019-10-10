import sys
import os
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
import shutil
import pandas as pd
import re
from tqdm import tqdm
basepass = sys.argv[1]

os.mkdir(basepass + "depth_mirror")
os.mkdir(basepass + "depth")
os.mkdir(basepass + "color_mirror")
os.mkdir(basepass + "color")
os.mkdir(basepass + "regi")
os.mkdir(basepass + "regi_mirror")
os.mkdir(basepass + "png")
os.mkdir(basepass + "jpg")
colorpass = glob.glob(basepass + "jpg_*")
print(colorpass)
for jpg_pass in tqdm(colorpass):
    jpg_images_pass = glob.glob(jpg_pass + "/*.jpg")
    print(jpg_images_pass)
    for image_pass in jpg_images_pass:
        pass_words = image_pass.split("/")
        shutil.copy2(image_pass, basepass + "jpg/" + pass_words[-1])

depthpass = glob.glob(basepass + "png_*")
for png_pass in tqdm(depthpass):
    png_images_pass = glob.glob(png_pass + "/*.png")
    for image_pass in png_images_pass:
        pass_words = image_pass.split("/")
        shutil.copy2(image_pass, basepass + "png/" + pass_words[-1])

imagepass = sys.argv[1] + "/png/*.png"
image_file_list = glob.glob(imagepass)
image_file_list.sort()

i = 0
second = 0
#前段階のフレームの数を最初は0に設定
beforeNum = 0
depthpass =  sys.argv[1] + "/depth/"
colorpass = sys.argv[1] + "/color/"
fileNumberList = list()
fileNumbertxt = list()
for ImageName in tqdm(image_file_list):

    Num = re.split('[._]',ImageName)
    Image = cv2.imread(ImageName,2)
    if int(int(Num[-2]) > beforeNum):
        #filename = str(second) + "." + str(round(float(Num[-2])/30,3))
        fileNumber = float(second) + float(Num[-2])/30
        #print(fileNumber)
        fileNumberList.append(round(fileNumber*30,0))
        fileNumbertxt.append(fileNumber)
        cv2.imwrite(depthpass + str(i).zfill(10) + '.png',Image)
        beforeNum = int(Num[-2])
        i += 1
    else:
        second+=1
        fileNumber = float(second) + float(Num[-2])/30
        #print(fileNumber)
        fileNumberList.append(round(fileNumber*30,0))
        fileNumbertxt.append(fileNumber)
        cv2.imwrite(depthpass + str(i).zfill(10) + '.png',Image)
        beforeNum = int(Num[-2])
        i += 1
jpgpass = sys.argv[1] + "/jpg/*.jpg"
jpg_file_list = glob.glob(jpgpass)
jpg_file_list.sort()
InitialNum = round(float(fileNumberList[0]), 0)
print("最初の数字は" + str(InitialNum))
j = 0
for JpgName in tqdm(jpg_file_list):
    """
    if InitialNum in fileNumberList:
        print("今回は" + str(InitialNum) + "を見ました")
        print("いまマッチングした数は" + str(InitialNum))
        #print(round(int(InitialNum)/30,3))
        filenumber2 = round(int(InitialNum)/30,3)
        color  = cv2.imread(JpgName)
        #print(type(color))
        cv2.imwrite(colorpass + str(j).zfill(10) + '.jpg',color)
        j += 1
    InitialNum += 1
    """
    color  = cv2.imread(JpgName)
    cv2.imwrite(colorpass + str(j).zfill(10) + '.jpg',color)
    j += 1

#print("hello")
df = pd.DataFrame(fileNumberList)
df.to_csv("/home/kei/document/experiments/Hamano/H5test/time.csv")
#数が二枚合わない。→多分、最初のdepthの枚数があってないことが問題。
