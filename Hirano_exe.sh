echo "yattyae!"
echo "FOR HIRANO"
#実行するディレクトリは/KeiHirano/
#実行前に
#chmod +x Hirano_exe.sh
#で実行権限を与える
#実行前の段階で，画像の初期位置を合わせたregiというファイルができているところからスタート
basepath="/home/kei/document/experiments/Hamano/shoda/"
openposeExeFile="./build/examples/openpose/openpose.bin"
dx=3 #アフィン変換させる場合の並進成分
mkdir ${basepath}/color2/
<< COMMENTOUT
解析に際して，記録しているdepth画像の枚数と，color画像の枚数が大幅にずれている場合，
画像解析(画像内である物体が動き出した瞬間や被験者が動き出した瞬間を確認して合わせる)
を用いてdepthとcolorの初期位置を合わせている．
そのため，この処理に関しては出来上がった画像を逐次的に確認する必要が有るため，
この部分は基本的にコメントアウト
echo "DepthMapper.cpp"
/usr/bin/g++ -g C++script/DepthMapper.cpp  -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/shoda/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/shoda/freenect2/lib -lfreenect2 -o C++script/DepthMapper
C++script/DepthMapper $basepath
COMMENTOUT
#color画像にアフィン変換をかけることにより，colorとdepthのズレの少ない
#綺麗なレジストレーション画像を作成する．
read -p "Please input Image_num:" Image_num
echo "fix_click.cpp"
/usr/bin/g++ -g C++script/fix_click.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -o C++script/fix_click
C++script/fix_click $basepath $Image_num
echo "click_plot.py"
python3 pythonscript/ImageTool/click_plot.py $basepath $Image_num
echo "depth_click.cpp"
/usr/bin/g++ -g C++script/depth_click.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -o C++script/depth_click
C++script/depth_click $basepath $Image_num
echo "check_click.py"
python3 pythonscript/ImageTool/check_click.py $basepath
echo "fixcolor.py"
python3 pythonscript/ImageTool/fixcolor.py $basepath
echo "FixMapper.cpp"
/usr/bin/g++ -g C++script/FixMapper.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/kei/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/kei/freenect2/lib -lfreenect2 -o C++script/FixMapper
C++script/FixMapper $basepath
echo "pngmirror.py"
python3 pythonscript/ImageTool/pngmirror.py $basepath


echo "***OpenPose***"

cd /home/kei/openpose
$openposeExeFile --image_dir ${basepath}regi_mirror/ -write_images ${basepath}render/ --write_json ${basepath}json/
cd /home/kei/document/KeiHirano

echo "showOpenPoseResult.py"
echo "Please check the result of openpose (press any key)"
python3 pythonscript/OpenPose/showOpenPoseResult_Hirano.py $basepath

echo "csvposer.py"
read -p "Please input PeopleID:" id
read -p "Please input startframe:" startframe
read -p "Please input endframe:" endframe
python3 pythonscript/csvpose/csvposer.py $basepath $id $startframe $endframe

echo "showCSVResult.py"
echo "Please check the result of people${id} (press any key)"
python3 pythonscript/OpenPose/showCSVResult.py ${basepath}regi_mirror/

<< COMMENTOUT
kinectの推定関節と，openposeの推定関節の位置のズレを二次元平面上で計算するスクリプト
echo "joint_diff.py"
python3 pythonscript/ImageTool/joint_diff.py ${basepath}
COMMENTOUT
echo "3DPoseMaker.cpp"
/usr/bin/g++ -g C++script/3DPoseMaker.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/kei/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/kei/freenect2/lib -lfreenect2 -o C++script/3DPoseMaker
C++script/3DPoseMaker $basepath $((endframe - startframe+1))

echo "Column.py"
python3 pythonscript/Liner/Column.py ${basepath}

echo "3DInterrupt.py"
echo "Do you want to Linear interpolation?: [Y/n]"
read ANSWER2
case $ANSWER2 in
    "" | "Y" | "y" | "yes" | "Yes" | "YES" ) python pythonscript/Liner/3DInterrupt.py ${basepath};;
esac

echo "BoundMaker_Hirano.cpp"
echo "Choose 10 points"
/usr/bin/g++ -g C++script/BoundMaker_Hirano.cpp -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/kei/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/kei/freenect2/lib -lfreenect2 -o C++script/BoundMaker_Hirano
C++script/BoundMaker_Hirano $basepath $Image_num

echo "3DChair.cpp"
/usr/bin/g++ -g C++script/3DChair.cpp  -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/kei/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/kei/freenect2/lib -lfreenect2 -o C++script/3DChair
C++script/3DChair $basepath $Image_num

echo "FixProductaxis.py"
python3 pythonscript/GroundCal/FixProductaxis.py ${basepath}

echo "Do you want to open Blender?: [Y/n]"
read ANSWER3
case $ANSWER3 in
    "" | "Y" | "y" | "yes" | "Yes" | "YES" ) blender;;
esac
