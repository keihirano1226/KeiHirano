import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import glob
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter('output.avi', fourcc, 30, (1920, 1080))

#fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
#video = cv2.VideoWriter('registered.mp4', fourcc, 20.0, (512, 424))
imageFilelist = glob.glob(sys.argv[1]+"/*")
imageFilelist.sort()
#print(imageFilelist)
i = 1
for imagename in imageFilelist:
    print(i)
    if i > 0 and i < 11000 :

        #print (i)
        img = cv2.imread(imagename)
        video.write(img)
    i = i + 1
video.release()
