import sys
import glob
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import os
import re
#これまでは、ファイル名にそのまま経過した秒数をつけていたが、
#秒数を.txtに保存して、ファイル名を0埋め.jpgにするように変更を加える。
imagepass = "/home/kei/document/experiments/2019.02.27.test/png_20180126112051/*.png"
image_file_list = glob.glob(imagepass)
image_file_list.sort()

i = 0
second = 0
#前段階のフレームの数を最初は0に設定
beforeNum = 0
depthpass = '/home/kei/document/experiments/2019.02.27.test/depth/'
colorpass = '/home/kei/document/experiments/2019.02.27.test/color/'
fileNumberList = list()
for ImageName in image_file_list:

    Num = re.split('[._]',ImageName)
    Image = cv2.imread(ImageName,2)
    if int(int(Num[-2]) > beforeNum):
        #filename = str(second) + "." + str(round(float(Num[-2])/30,3))
        fileNumber = float(second) + float(Num[-2])/30
        print(fileNumber)
        fileNumberList.append(round(fileNumber*30,0))
        cv2.imwrite(depthpass + '{:.3f}'.format(fileNumber) + '.png',Image)
        beforeNum = int(Num[-2])
    else:
        second+=1
        fileNumber = float(second) + float(Num[-2])/30
        print(fileNumber)
        fileNumberList.append(round(fileNumber*30,0))
        cv2.imwrite(depthpass + '{:.3f}'.format(fileNumber) + '.png',Image)
        beforeNum = int(Num[-2])
jpgpass = "/home/kei/document/experiments/2019.02.27.test/jpg_20180126112051/*.jpg"
jpg_file_list = glob.glob(jpgpass)
jpg_file_list.sort()
InitialNum = round(float(fileNumberList[0]), 0)
print(InitialNum)

for JpgName in jpg_file_list:

    if InitialNum in fileNumberList:
        print(round(int(InitialNum)/30,3))
        filenumber2 = round(int(InitialNum)/30,3)
        color  = cv2.imread(JpgName)
        print(type(color))
        cv2.imwrite(colorpass + '{:.3f}'.format(filenumber2) + '.jpg',color)
    InitialNum += 1
print("hello")
print(fileNumberList)
