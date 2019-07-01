import sys
import glob
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import os
import re
import pandas as pd
#これまでは、ファイル名にそのまま経過した秒数をつけていたが、
#秒数を.txtに保存して、ファイル名を0埋め.jpgにするように変更を加える。
#renameを行うプログラムは基本的にはこっち。
#basepass = sys.argv[1]
imagepass = "/home/kei/document/experiments/2019.06.25/data3/png/*.png"
image_file_list = glob.glob(imagepass)
image_file_list.sort()

i = 0
second = 0
#前段階のフレームの数を最初は0に設定
beforeNum = 0
depthpass = '/home/kei/document/experiments/2019.06.25/data3/depth/'
colorpass = '/home/kei/document/experiments/2019.06.25/data3/color/'
fileNumberList = list()
fileNumbertxt = list()
for ImageName in image_file_list:

    Num = re.split('[._]',ImageName)
    Image = cv2.imread(ImageName,2)
    #filename = str(second) + "." + str(round(float(Num[-2])/30,3))
    fileNumber = float(second) + float(Num[-2])/30
    #print(fileNumber)
    fileNumberList.append(round(fileNumber*30,0))
    fileNumbertxt.append(fileNumber)
    cv2.imwrite(depthpass + str(i).zfill(10) + '.png',Image)
    beforeNum = int(Num[-2])
    i += 1
jpgpass = "/home/kei/document/experiments/2019.06.25/data3/jpg/*.jpg"
jpg_file_list = glob.glob(jpgpass)
jpg_file_list.sort()
j = 0
for JpgName in jpg_file_list:

    color  = cv2.imread(JpgName)
    #print(type(color))
    cv2.imwrite(colorpass + str(j).zfill(10) + '.jpg',color)
    j += 1
    #InitialNum += 1

#print("hello")
df = pd.DataFrame(fileNumberList)
df.to_csv("/home/kei/document/experiments/2019.06.25/data3/time.csv")
#数が二枚合わない。→多分、最初のdepthの枚数があってないことが問題。
