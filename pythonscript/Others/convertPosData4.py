# -*- coding:utf-8 -*-
import struct
import sys
import glob
import os
import zipfile
if sys.version_info.major ==2:
     import cStringIO
else:
     import io as cStringIO




def fixBadZipfile(zipFile):  
     f = open(zipFile, 'r+b')  
     data = f.read()  
     pos = data.find('\x50\x4b\x05\x06') # End of central directory signature  
     if (pos > 0):  
         self._log("Truncating file at location " + str(pos + 22) + ".")  
         f.seek(pos + 22)   # size of 'ZIP end of central directory record' 
         f.truncate()  
         f.close()  

def convertToCSV(zipFileName,outputFileName):
    if os.path.exists(outputFileName):
        return
    
    output = open(outputFileName,'w')

    if not zipfile.is_zipfile(zipFileName):
        print("not zip file") 
        return

    print(zipFileName)
    
    frameIndex = 0
    frameNumber = -1
    with zipfile.ZipFile(zipFileName, 'r') as post:
        for info in post.infolist():
            if sys.version_info.major ==2:
                 buf = ""
                 f = cStringIO.StringIO(post.read(info.filename))
            else:
                 buf = b""
                 f = cStringIO.BytesIO(post.read(info.filename))
            
            for line in f:
                buf += line


            fn = info.filename.split("_")[2]
            fn = int(fn.replace(".pos",""))
            step = 1
            if frameNumber != -1:
                while fn < frameNumber:
                    fn += 30
                step = fn - frameNumber
            fn = info.filename.split("_")[2]
            fn = int(fn.replace(".pos",""))
            frameNumber = fn
            dataCount = int(len(buf)/308)
#            print "DataCount:"+str(dataCount)
            frameIndex += step
            for j in range(0,dataCount):
                output.write(str(frameIndex))
                output.write(",")
                index = 0 + j*308
                val = struct.unpack("Q",buf[index:index+8])
#                print "ID:"+str(val[0])
                output.write(str(val[0]))
                output.write(",")

                
                for i in range(1,26):
                    index = j*308+ 8+(i-1)*(12)
                    xVal=buf[index:index+4]
                    xVal = struct.unpack("f",xVal)
                    index = index+4
                    yVal=buf[index:index+4]
                    yVal = struct.unpack("f",yVal)
                    index = index+4
                    zVal=buf[index:index+4]

                    zVal = struct.unpack("f",zVal)
                    output.write(str(xVal[0]))
                    output.write(",")
                    output.write(str(yVal[0]))
                    output.write(",")
                    output.write(str(zVal[0]))
                    output.write(",")

                output.write("\n")
    output.close()


def extractFromList(list,keyword):
    ret = [];
    for i in range(len(list)):
        if keyword in list[i]:
            ret.append(list[i])
    return ret







'''
print "Select a type of the specified folder from the following 1, 2, 3."
print "1: "The specified folder"/MonthDayFolder/YearMonthDayHourMin.Sec._IP/ (In case of after running DataArrangement.py)")
print("2: "The specified folder"/MonthDayFolder/YearMonthDayHourMin.Sec._IP/")
print("3: "The specified folder"/zip files")
'''
print(u"指定したフォルダの下の構成を、以下の1～3から選択してください。")
print(u"1: 指定したフォルダ/月日のフォルダ/年月日時間分秒_IPのフォルダがある場合（DataArrangement.py実行後の場合）")
print(u"2: 指定したフォルダ/年月日時間分秒_IPのフォルダがある場合")
print(u"3: 指定したフォルダの下に、zipファイルがある場合")
mode = int(input())

if mode == 1:
     dirList = glob.glob(sys.argv[1]+"/*")

     dataDirList=[]
     for dirName in dirList:
         dataDirList += glob.glob(dirName+"/*")


     for dirName in dataDirList:
         fileList = glob.glob(dirName+"/*")
         fileList = extractFromList(fileList,"pos")
         fileList = extractFromList(fileList,".zip")

         for fileName in fileList:
             outputFileName = fileName.replace(".zip",".csv")
             convertToCSV(fileName,outputFileName)
elif mode == 2:
     dirList = glob.glob(sys.argv[1]+"/*")
     fileList = []
     for dir in dirList:
          fileList.extend(glob.glob(dir+"/*"))
          
     fileList = extractFromList(fileList,"pos")
     fileList = extractFromList(fileList,".zip")

     for fileName in fileList:
         outputFileName = fileName.replace(".zip",".csv")
         convertToCSV(fileName,outputFileName)

elif mode == 3:
     
     fileList = glob.glob(sys.argv[1]+"/*")
     fileList = extractFromList(fileList,"pos")
     fileList = extractFromList(fileList,".zip")

     for fileName in fileList:
         outputFileName = fileName.replace(".zip",".csv")
         convertToCSV(fileName,outputFileName)

     

