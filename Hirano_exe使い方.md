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
<br>
[click_plot.py](pythonscript/ImageTool/click_plot.py)
__入力__basepath Image_num
__出力__regi_2d_points.csv
