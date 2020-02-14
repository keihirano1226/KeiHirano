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

4. 補間された姿勢データに対して最後にフィルタ処理を行う  
[3Dkalman.py](pythonscript/Filter/33Dkalman.py)  
__入力__basepath  
__出力__3DFiltered.csv  
5. もし，姿勢データが左手を中心としたものだった場合には5の処理が必要になる．姿勢を左右反転させて対応する関節のIDを反転させる処理．  
[LRchange.py](pythonscript/GroundCal/LRchange.py)  
__入力__basepath  
__出力__3DFiltered2.csv  
## 簡易作業フロー(3):変化点検出
1. 作成した動作に対して変化点検出を用いて動作の開始点と終了点を決める．変化点検出では時間幅などのパラメータは出力結果などを見ながら確認していく必要があるので，パラメータを0.1秒から0.5秒まで0.1秒刻みで変化させるプログラムを作成した．
[cf_svd.py](pythonscript/Changefinder/cf_svd.py)  
__入力__basepath  
__出力__各時間幅での開始終了に関する変化を表したグラフの画像,  
それぞれの値を書いたcsv(end_cf_score.csv,end_diff_cf_score.csv,start_cf_score.csv,start_diff_cf_score.csv)  
この辺の結果を見ながら開始時刻，終了時刻に関して決定を行う．

2. 3DFiltered.csvのファイルを開始終了時刻に合わせて切り取り，ファイル名を動作IDに変更した後解析フォルダ(今回の場合はMaster2)に移動させる．

## 簡易作業フロー(4):クラスタリング
1. 解析フォルダに移動させた動作データについて解析を行う．解析前に"Unified"と"AJ_result"については解析用フォルダ内にフォルダを作成しておくこと.使いたい関節のセット(上半身だけとか左半身だけとか)を作成したい場合は/mapper/BodyColumnに新しい関節セットを作って14行目で上手いこと読み込んで下さい．    
[Master_Mapper.py](pythonscript/mapper/Master_Mapper.py)  

## 簡易作業フロー(5):マップ作成
1. 距離行列を使って多次元尺度構成法でマップを作成する．この時作成するマップを何と関連付けるか(製品か認知能力か身体能力か)は全てコメントアウトの外し方で調整していました．
[Master_MDS.py]

## 簡易作業フロー(6):クラスタ平均動作の作成
1. 分類された各クラスタの平均動作を作成する．  
[Master_average.py](pythonscript/mapper/Master_average.py)
2. それぞれのクラスタの動作を同一製品座標系の動作として描画する．動画の作成の際に，画像として一枚ずつ吐き出したい場合は112行目あたりからいじるべし．また読み込み元のcsvファイルによって14，15行目の関節セットの書き方が変わるので注意．  
[2pose_All.py](pythonscript/plot/2pose_All.py)
