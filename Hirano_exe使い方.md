# Hirano_exe使い方
実行時点で，
basepath/  
┠  color  
┠  color2    
┠  depth  
┠  depth_mirror  
┠  pos  
┠  regi  
┠  regi2      
┗  regi_mirror  
のフォルダが出来ており，colorDirとdepthDir，regiDirにそれぞれ画像が入っている.
製品座標系の決定及びレジストレーション画像の修正に使う画像は同じであるため，実行前にどの画像を使って行うかを決定しておく．
また実行前に解析対象となるファイルのパスを変更しておく(8行目)
## 実行フロー

1. マウス手動計測によるアフィン変換パラメータの取得  
[fix_click.cpp](C++script/fix_click.cpp)
__入力__basepath Image_num  
__出力__regi_2d_points.csv    
2. 手動計測した結果を画像で出力する．  
[click_plot.py](pythonscript/ImageTool/click_plot.py)    
__入力__basepath Image_num  
__出力__regi_2d_points.csv  

3. 先ほどクリックで指定した点に対応する奥行き画像上の対応点をクリックで指定する．  
[depth_click.cpp](C++script/depth_click.cpp)  
__入力__basepath Image_num  
__出力__depth_2d_points.csv  

4. color画像をアフィン変換するためのパラメータを計算しアフィン変換を行う．  
[fixcolor.py](pythonscript/fixcolor.py)  
__入力__basepath  
__出力__color2 diff.csv diff_mean.csv    

5. color画像をアフィン変換するためのパラメータを計算しアフィン変換を行う．  
[FixMapper.cpp](C++script/FixMapper.cpp)  
__入力__basepath  
__出力__regi2  

6. color画像をアフィン変換するためのパラメータを計算しアフィン変換を行う．  
[pngmirror.py](C++script/FixMapper.cpp)  
__入力__basepath  
__出力__regi2　　

7. openposeの実行を行う．  

8. 出力されたopenposeの出力を確認できるスクリプト．ココで，解析に使用するフレーム，及び解析開始フレームにおける対象被験者のIDを確認しておく．  
[showOpenPoseResult_Hirano.py](pythonscript/OpenPose/showOpenPoseResult_Hirano.py)   
__入力__basepath  

9. 一つ前のスクリプトで確認した開始，終了フレーム，及び対象被験者のID番号を引数として与えてjson内の姿勢データから対象被験者のデータのみ抽出しcsvファイルにまとめる．  
[csvposer.py](pythonscript/csvpose/csvposer.py)  
__入力__ID,開始フレーム，終了フレーム  
__出力__test.csv　　

10. csvposeに変換した二次元姿勢情報，及び奥行き情報を用いて三次元姿勢を生成する．  
[3DPoseMaker.cpp](C++script/3DPoseMaker.cpp)  
__入力__test.csv,Depth画像  
__出力__3dbone.csv  

11. 生成したテキストファイルにカラム名をつけて保存するためのスクリプト．  
[Column.py](pythonscript/Liner/Column.py)  
__入力__test.csv,Depth画像  
__出力__3dbone.csv  

12. 線形補間を行うスクリプト  
[3DInterrupt.py](pythonscript/Liner/3DInterrupt.py)  
__入力__3dbone.csv  
__出力__3DInterrupt.csv  

13. 製品座標系に変換を行うために5種類の点群を打つためのスクリプト．今回の場合，座面，背もたれとする点群の原点をそれぞれ選択する．この時領域選択の場合は，二次元画面内の左上と右下を選択するようにする．  
[BoundMaker_Hirano.cpp](C++script/BoundMaker_Hirano.cpp)  
__入力__レジストレーション画像1枚  
__出力__2DGround.csv  

14. それぞれ指定した領域の三次元点群データを取得する．  
[3DChair.cpp](C++script/3DChair.cpp)  
__入力__2DGround.csv  
__出力__Zplane.csv,Xplane.csv,edge.csv

15.　三次元姿勢データを製品座標系に座標変換するためのスクリプト．  
[FixProductaxis.py](pythonscript/GroundCal/FixProductaxis.py)  
__入力__basepath  
__出力__33dboneRotated.csv
