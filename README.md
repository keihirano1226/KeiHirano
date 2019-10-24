# KeiHirano
study and research
研究用のスクリプトを保存しておく場所．
Kinect及びdepthデータを扱う関係のスクリプトがC++の中に
それ以外のものは，pythonscriptの中に
pythonスクリプトは，基本的には扱うものとかで場合分けしている．
基本的にはタイトルのまんまのスクリプトであることが多い．

## 実験ディレクトリについては以下のフォルダ構成を守ること(2019/10/24現在)
basepath/  
┠  color  
┠  color_mirror  
┠  depth  
┠  depth_mirror  
┠  regi  
┠  regi_mirror  
┠  regi_mirror_fixed  
┠  render  
┗  render_fixed

## 簡易作業フロー
```
(colorとdepthがある状態)
DepthMapper.cpp
fixregi.py
OPENPOSE(render生成)
csvposer.py
showOpenPoseResult.py
showCSVResult.py
joint_diff.py
(続く)
```
