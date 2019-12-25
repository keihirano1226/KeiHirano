import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import glob
import os

import cv2

# VideoCapture を作成する。
output_dirpath = '/home/kei/document/experiments/Hamano/H4_2/face/'
img_path = os.path.join(output_dirpath)  # 画像ファイルのパス
cap = cv2.VideoCapture(img_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30
print('width: {}, height: {}, fps: {}'.format(width, height, fps))

# VideoWriter を作成する。
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
writer = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))
i = 0
while True:

    # 1フレームずつ取得する。
    ret, frame = cap.read()
    if not ret:
        break  # 映像取得に失敗
    if i >= 0:
        writer.write(frame)  # フレームを書き込む。
    i = i + 1
writer.release()
cap.release()
