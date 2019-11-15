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
__入力__color2  
__出力__regi2  

6. color画像をアフィン変換するためのパラメータを計算しアフィン変換を行う．  
[pngmirror.py](C++script/FixMapper.cpp)  
__入力__color2  
__出力__regi2
