# KeiHirano

## 掟
study and research
研究用のスクリプトを保存しておく場所．
Kinect及びdepthデータを扱う関係のスクリプトがC++の中に
それ以外のものは，pythonscriptの中に
pythonスクリプトは，基本的には扱うものとかで場合分けしている．
基本的にはタイトルのまんまのスクリプトであることが多い．

__作業フローに変更や追加があったらREADMEを更新すること__

## 実験ディレクトリについては以下のフォルダ構成を守ること(2019/11/15現在)
__予め以下のディレクトリを作っておくこと__
(初期状態はcolorDirとdepthDirとposは中身がある状態.その後正田方式を撮るか平野方式を取るかで出力されるファイルが異なる．)  
basepath/  
┠  color  
┠  color2  
┠  depth  
┠  depth_mirror  
┠  json  
┠  pos  
┠  regi  
┠  regi2    
┠  regi_mirror  
┠  regi_mirror_fixed  
┗  render

## 環境によるスクリプトの変更について
python関係のスクリプトで，ROSシステムが入っているせいで，
opencvのライブラリ使用時に追加で記述している部分が有る．
[showOpenPoseResult.py](/pythonscript/OpenPose/showOpenPoseResult.py)などは，ROS有りの環境で使用する際には，[showOpenPoseResult_Hirano.py](/pythonscript/OpenPose/showOpenPoseResult_Hirano.py)など若干名称を変更したものを使用すること．引数や出力などは変わらない．なので，こちらは本人の許可がない限り変更しないこと．

## 動作作成シェルスクリプト
[shoda_exe.sh](./shoda_exe.sh)
[Hirano_exe.sh](./Hirano_exe.sh)
両者でレジストレーション画像の生成方法に違いが有る．
[Hirano_exe.sh](./Hirano_exe.sh)内での処理や作業フローについては，[Hirano_exe使い方.md](./Hirano_exe使い方.md)を参照
## 簡易作業フロー(1):三次元動作生成

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
__入力__basepath  
__出力__3dbone.csv  

11. 生成したテキストファイルにカラム名をつけて保存するためのスクリプト．  
[Column.py](pythonscript/Liner/Column.py)  
__入力__basepath  
__出力__3dbone.csv  

12. 線形補間を行うスクリプト  
[3DInterrupt.py](pythonscript/Liner/3DInterrupt.py)  
__入力__basepath  
__出力__3DInterrupt.csv  

13. 製品座標系に変換を行うために5種類の点群を打つためのスクリプト．今回の場合，座面，背もたれとする点群の原点をそれぞれ選択する．この時領域選択の場合は，二次元画面内の左上と右下を選択するようにする．  
[BoundMaker_Hirano.cpp](C++script/BoundMaker_Hirano.cpp)  
__入力__basepath,注目する画像ファイル番号  
__出力__2DGround.csv  

14. それぞれ指定した領域の三次元点群データを取得する．  
[3DChair.cpp](C++script/3DChair.cpp)  
__入力__basepath,注目する画像番号  
__出力__Zplane.csv,Xplane.csv,edge.csv

15. 三次元姿勢データを製品座標系に座標変換するためのスクリプト．  
[FixProductaxis.py](pythonscript/GroundCal/FixProductaxis.py)  
__入力__basepath  
__出力__3dboneRotated.csv

## 簡易作業フロー(2):三次元動作の誤差修正など補間処理  
1. 生成した動作をまずはblenderで確認してみる．引き継ぎ史料上にあるblenderファイル内に読み込みを行うためのスクリプトが内蔵されているのでまずは開いてみるべし．このときエラーが出て開けない場合にはcsvファイルに空白があるなどの場合があるので，まずは確認．空白の部分に関しては0埋めしてもいいし，前後の値と同じものをとりあえず突っ込んで読み込めるようにしてもいいと思う．
2. 生成された動作データの問題が有る部分について一つずつ手作業で指定を行い修正を行っていく．基本的に目視で確認してダメそう明らかにおかしいなという部分に関しては，3dboRotated.csv上で編集を行い，とりあえず空欄にしていく．
3. 空欄がたくさん出来た3dborotated.csvについて線形補完を行う．  
[FilteredInterrupt.py](pythonscript/Liner/FilteredInterrupt.py)  
__入力__basepath  
__出力__3DInterrupt2.csv

3. 補間された姿勢データに対して最後にフィルタ処理を行う
__入力__basepath  
__出力__3DFiltered.csv  
4. もし，姿勢データが左手を中心としたものだった場合には4の処理が必要になる．姿勢を左右反転させて対応する関節のIDを反転させる処理．
__入力__basepath  
__出力__3DFiltered2.csv  
