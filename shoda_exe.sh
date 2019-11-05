echo "yattyae!"
echo "FOR SHODA"

basepath="/home/shoda/Documents/mitsu2/"
openposeExeFile="./build/examples/openpose/openpose.bin"
dx=3 #アフィン変換させる場合の並進成分

echo "DepthMapper.cpp"
/usr/bin/g++ -g C++script/DepthMapper.cpp  -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/shoda/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/shoda/freenect2/lib -lfreenect2 -o C++script/DepthMapper
C++script/DepthMapper $basepath

echo "regimirror.py"
python pythonscript/ImageTool/regimirror.py $basepath

echo "fixregi.py"
python pythonscript/ImageTool/fixregi.py $basepath $dx

echo "***OpenPose***"

cd /home/shoda/openpose
$openposeExeFile --image_dir ${basepath}regi_mirror_fixed -write_images ${basepath}render --write_json ${basepath}json
cd /home/shoda/KeiHirano

echo "showOpenPoseResult.py"
echo "Please check the result of openpose (press any key)"
python pythonscript/OpenPose/showOpenPoseResult.py $basepath

echo "csvposer.py"
read -p "Please input PeopleID:" id
read -p "Please input startframe:" startframe
read -p "Please input endframe:" endframe
python pythonscript/csvpose/csvposer.py $basepath $id $startframe $endframe

echo "showCSVResult.py"
echo "Please check the result of people${id} (press any key)"
python pythonscript/OpenPose/showCSVResult.py ${basepath}regi_mirror_fixed ${basepath}output.csv

echo "joint_diff.py"
python pythonscript/ImageTool/joint_diff.py ${basepath}

echo "3DPoseMaker.cpp"
/usr/bin/g++ -g C++script/3DPoseMaker.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/shoda/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/shoda/freenect2/lib -lfreenect2 -o C++script/3DPoseMaker
C++script/3DPoseMaker $basepath

echo "Column.py"
python pythonscript/Liner/Column.py ${basepath}

echo "3DInterrupt.py"
echo "Do you want to Linear interpolation?: [Y/n]"
read ANSWER2
case $ANSWER2 in
    "" | "Y" | "y" | "yes" | "Yes" | "YES" ) python pythonscript/Liner/3DInterrupt.py ${basepath};;
esac

echo "BoundMaker.cpp"
echo "Choose 10 points"
/usr/bin/g++ -g C++script/BoundMaker.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -o C++script/BoundMaker
C++script/BoundMaker $basepath

echo "3DChair.cpp"
/usr/bin/g++ -g C++script/3DChair.cpp  -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/shoda/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/shoda/freenect2/lib -lfreenect2 -o C++script/3DChair
C++script/3DChair $basepath

echo "CalProductaxis.py"
python pythonscript/GroundCal/CalProductaxis.py ${basepath}

echo "Do you want to open Blender?: [Y/n]"
read ANSWER3
case $ANSWER3 in
    "" | "Y" | "y" | "yes" | "Yes" | "YES" ) blender;;
esac