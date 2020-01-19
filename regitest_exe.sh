echo "yattyae!"
echo "FOR HIRANO"
#実行するディレクトリは/KeiHirano/
#実行前に
#chmod +x regitest_exe.sh
#画像のスタート位置を決めるためのシェルスクリプト
basepath="/home/kei/document/experiments/Hamano/shoda/"
folder1=regi
if [ ! -d ${basepath%/}${folder1} ]; then
  mkdir ${basepath}/regi
fi
folder2=color
if [ ! -d ${basepath%/}${folder2} ]; then
  mkdir ${basepath}/color
fi
folder3=depth
if [ ! -d ${basepath%/}${folder3} ]; then
  mkdir ${basepath}/depth
fi
folder4=color_mirror
if [ ! -d ${basepath%/}${folder4} ]; then
  mkdir ${basepath}/color_mirror
fi
folder5=depth_mirror
if [ ! -d ${basepath%/}${folder5} ]; then
  mkdir ${basepath}/depth_mirror
fi
folder6=regi_mirror
if [ ! -d ${basepath%/}${folder6} ]; then
  mkdir ${basepath}/regi_mirror
fi
folder7=regi2
if [ ! -d ${basepath%/}${folder7} ]; then
  mkdir ${basepath}/regi2
fi
folder8=jpg
if [ ! -d ${basepath%/}${folder7} ]; then
  mkdir ${basepath}/jpg
fi
folder9=jpg
if [ ! -d ${basepath%/}${folder9} ]; then
  mkdir ${basepath}/png
fi
echo "jpg2color&png2depth.py"
python3 pythonscript/ImageTool/jpg2color_png2depth.py $basepath

echo "DepthMapper.cpp"
/usr/bin/g++ -g C++script/DepthMapper.cpp  -I/usr/local/include/opencv2 -I/usr/local/include/opencv -I/home/kei/freenect2/include -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc -L/home/kei/freenect2/lib -lfreenect2 -o C++script/DepthMapper
C++script/DepthMapper $basepath

echo "test"
